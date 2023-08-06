"""Core class for the Daymet functions."""
from typing import Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import py3dep
import shapely.geometry as sgeom
import xarray as xr
from pydantic import BaseModel, validator

from .exceptions import InvalidInputRange, InvalidInputType, InvalidInputValue, MissingItems

DEF_CRS = "epsg:4326"
DATE_FMT = "%Y-%m-%d"


class DaymetBase(BaseModel):
    """Base class for validating Daymet requests.

    Parameters
    ----------
    pet : bool, optional
        Whether to compute evapotranspiration based on
        `UN-FAO 56 paper <http://www.fao.org/3/X0490E/x0490e06.htm>`__.
        The default is False
    time_scale : str, optional
        Data time scale which can be daily, monthly (monthly summaries),
        or annual (annual summaries). Defaults to daily.
    variables : list, optional
        List of variables to be downloaded. The acceptable variables are:
        ``tmin``, ``tmax``, ``prcp``, ``srad``, ``vp``, ``swe``, ``dayl``
        Descriptions can be found `here <https://daymet.ornl.gov/overview>`__.
        Defaults to None i.e., all the variables are downloaded.
    region : str, optional
        Region in the US, defaults to na. Acceptable values are:

        * na: Continental North America
        * hi: Hawaii
        * pr: Puerto Rico
    """

    pet: bool = False
    time_scale: str = "daily"
    variables: List[str] = ["all"]
    region: str = "na"

    @validator("variables")
    def _valid_variables(cls, v, values) -> List[str]:
        valid_variables = ["dayl", "prcp", "srad", "swe", "tmax", "tmin", "vp"]
        if "all" in v:
            return valid_variables

        variables = [v] if isinstance(v, str) else v

        if not set(variables).issubset(set(valid_variables)):
            raise InvalidInputValue("variables", valid_variables)

        if values["pet"]:
            variables = list({"tmin", "tmax", "srad", "dayl"} | set(variables))
        return variables

    @validator("time_scale")
    def _valid_timescales(cls, v, values):
        valid_timescales = ["daily", "monthly", "annual"]
        if v not in valid_timescales:
            raise InvalidInputValue("time_scale", valid_timescales)

        if values["pet"] and v != "daily":
            msg = "PET can only be computed at daily scale i.e., time_scale must be daily."
            raise InvalidInputRange(msg)
        return v

    @validator("region")
    def _valid_regions(cls, v):
        valid_regions = ["na", "hi", "pr"]
        if v not in valid_regions:
            raise InvalidInputValue("region", valid_regions)
        return v


class Daymet:
    """Base class for Daymet requests.

    Parameters
    ----------
    variables : str or list or tuple, optional
        List of variables to be downloaded. The acceptable variables are:
        ``tmin``, ``tmax``, ``prcp``, ``srad``, ``vp``, ``swe``, ``dayl``
        Descriptions can be found `here <https://daymet.ornl.gov/overview>`__.
        Defaults to None i.e., all the variables are downloaded.
    pet : bool, optional
        Whether to compute evapotranspiration based on
        `UN-FAO 56 paper <http://www.fao.org/3/X0490E/x0490e06.htm>`__.
        The default is False
    time_scale : str, optional
        Data time scale which can be daily, monthly (monthly summaries),
        or annual (annual summaries). Defaults to daily.
    region : str, optional
        Region in the US, defaults to na. Acceptable values are:

        * na: Continental North America
        * hi: Hawaii
        * pr: Puerto Rico
    """

    def __init__(
        self,
        variables: Optional[Union[Iterable[str], str]] = None,
        pet: bool = False,
        time_scale: str = "daily",
        region: str = "na",
    ) -> None:

        _variables = ["all"] if variables is None else variables
        _variables = [_variables] if isinstance(_variables, str) else _variables
        validated = DaymetBase(variables=_variables, pet=pet, time_scale=time_scale, region=region)
        self.variables = validated.variables
        self.pet = validated.pet
        self.time_scale = validated.time_scale
        self.region = validated.region

        self.region_bbox = {
            "na": sgeom.box(-136.8989, 6.0761, -6.1376, 69.077),
            "hi": sgeom.box(-160.3055, 17.9539, -154.7715, 23.5186),
            "pr": sgeom.box(-67.9927, 16.8443, -64.1195, 19.9381),
        }
        self.invalid_bbox_msg = "\n".join(
            [
                f"Input coordinates are outside the Daymet range for region ``{region}``.",
                f"Valid bounding box is: {self.region_bbox[region].bounds}",
            ]
        )
        if self.region == "pr":
            self.valid_start = pd.to_datetime("1950-01-01")
        else:
            self.valid_start = pd.to_datetime("1980-01-01")
        self.valid_end = pd.to_datetime("2020-12-31")
        self._invalid_yr = (
            "Daymet database ranges from " + f"{self.valid_start.year} to {self.valid_end.year}."
        )
        self.time_codes = {"daily": 1840, "monthly": 1855, "annual": 1852}

        self.daymet_table = pd.DataFrame(
            {
                "Parameter": [
                    "Day length",
                    "Precipitation",
                    "Shortwave radiation",
                    "Snow water equivalent",
                    "Maximum air temperature",
                    "Minimum air temperature",
                    "Water vapor pressure",
                ],
                "Abbr": ["dayl", "prcp", "srad", "swe", "tmax", "tmin", "vp"],
                "Units": ["s/day", "mm/day", "W/m2", "kg/m2", "degrees C", "degrees C", "Pa"],
                "Description": [
                    "Duration of the daylight period in seconds per day. "
                    + "This calculation is based on the period of the day during which the "
                    + "sun is above a hypothetical flat horizon",
                    "Daily total precipitation in millimeters per day, sum of"
                    + " all forms converted to water-equivalent. Precipitation occurrence on "
                    + "any given day may be ascertained.",
                    "Incident shortwave radiation flux density in watts per square meter, "
                    + "taken as an average over the daylight period of the day. "
                    + "NOTE: Daily total radiation (MJ/m2/day) can be calculated as follows: "
                    + "((srad (W/m2) * dayl (s/day)) / l,000,000)",
                    "Snow water equivalent in kilograms per square meter."
                    + " The amount of water contained within the snowpack.",
                    "Daily maximum 2-meter air temperature in degrees Celsius.",
                    "Daily minimum 2-meter air temperature in degrees Celsius.",
                    "Water vapor pressure in pascals. Daily average partial pressure of water vapor.",
                ],
            }
        )

        self.units = dict(zip(self.daymet_table["Abbr"], self.daymet_table["Units"]))

    @staticmethod
    def check_dates(dates: Union[Tuple[str, str], Union[int, List[int]]]) -> None:
        """Check if input dates are in correct format and valid."""
        if not isinstance(dates, (tuple, list, int)):
            raise InvalidInputType(
                "dates", "tuple, list, or int", "(start, end), year, or [years, ...]"
            )

        if isinstance(dates, tuple) and len(dates) != 2:
            raise InvalidInputType(
                "dates", "Start and end should be passed as a tuple of length 2."
            )

    def dates_todict(self, dates: Tuple[str, str]) -> Dict[str, str]:
        """Set dates by start and end dates as a tuple, (start, end)."""
        if not isinstance(dates, tuple) or len(dates) != 2:
            raise InvalidInputType("dates", "tuple", "(start, end)")

        start = pd.to_datetime(dates[0])
        end = pd.to_datetime(dates[1])

        if start < self.valid_start or end > self.valid_end:
            raise InvalidInputRange(self._invalid_yr)

        return {
            "start": start.strftime(DATE_FMT),
            "end": end.strftime(DATE_FMT),
        }

    def years_todict(self, years: Union[List[int], int]) -> Dict[str, str]:
        """Set date by list of year(s)."""
        years = [years] if isinstance(years, int) else years

        if min(years) < self.valid_start.year or max(years) > self.valid_end.year:
            raise InvalidInputRange(self._invalid_yr)

        return {"years": ",".join(str(y) for y in years)}

    def dates_tolist(
        self, dates: Tuple[str, str]
    ) -> List[Tuple[pd.DatetimeIndex, pd.DatetimeIndex]]:
        """Correct dates for Daymet accounting for leap years.

        Daymet doesn't account for leap years and removes Dec 31 when
        it's leap year.

        Parameters
        ----------
        dates : tuple
            Target start and end dates.

        Returns
        -------
        list
            All the dates in the Daymet database within the provided date range.
        """
        date_dict = self.dates_todict(dates)
        start = pd.to_datetime(date_dict["start"]) + pd.DateOffset(hour=12)
        end = pd.to_datetime(date_dict["end"]) + pd.DateOffset(hour=12)

        period = pd.date_range(start, end)
        nl = period[~period.is_leap_year]
        lp = period[(period.is_leap_year) & (~period.strftime(DATE_FMT).str.endswith("12-31"))]
        _period = period[(period.isin(nl)) | (period.isin(lp))]
        years = [_period[_period.year == y] for y in _period.year.unique()]
        return [(y[0], y[-1]) for y in years]

    def years_tolist(
        self, years: Union[List[int], int]
    ) -> List[Tuple[pd.DatetimeIndex, pd.DatetimeIndex]]:
        """Correct dates for Daymet accounting for leap years.

        Daymet doesn't account for leap years and removes Dec 31 when
        it's leap year.

        Parameters
        ----------
        years: list
            A list of target years.

        Returns
        -------
        list
            All the dates in the Daymet database within the provided date range.
        """
        date_dict = self.years_todict(years)
        start_list, end_list = [], []
        for year in date_dict["years"].split(","):
            s = pd.to_datetime(f"{year}0101")
            start_list.append(s + pd.DateOffset(hour=12))
            if int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
                end_list.append(pd.to_datetime(f"{year}1230") + pd.DateOffset(hour=12))
            else:
                end_list.append(pd.to_datetime(f"{year}1231") + pd.DateOffset(hour=12))
        return list(zip(start_list, end_list))

    @staticmethod
    def pet_bycoords(
        clm_df: pd.DataFrame,
        coords: Tuple[float, float],
        crs: str = DEF_CRS,
        alt_unit: bool = False,
    ) -> pd.DataFrame:
        """Compute Potential EvapoTranspiration using Daymet dataset for a single location.

        Notes
        -----
        The method is based on
        `FAO Penman-Monteith equation <http://www.fao.org/3/X0490E/x0490e06.htm>`__
        assuming that soil heat flux density is zero.

        Parameters
        ----------
        clm_df : DataFrame
            The dataset must include at least the following variables:
            ``tmin (deg c)``, ``tmax (deg c)``, ``srad (W/m^2)``, and ``dayl (s)``.
            Also, if ``rh (-)`` (relative humidity) and ``u2 (m/s)`` (wind at 2 m level)
            are available, they are used. Otherwise, actual vapour pressure is assumed
            to be saturation vapour pressure at daily minimum temperature and 2-m wind
            speed is considered to be 2 m/s.
        coords : tuple of floats
            Coordinates of the daymet data location as a tuple, (x, y).
        crs : str, optional
            The spatial reference of the input coordinate, defaults to epsg:4326.
        alt_unit : str, optional
            Whether to use alternative units rather than the official ones, defaults to False.

        Returns
        -------
        pandas.DataFrame
            The input DataFrame with an additional column named ``pet (mm/day)``
        """
        units = {
            "srad": ("W/m2", "W/m^2"),
            "temp": ("degrees C", "deg c"),
        }

        tmin_c = f"tmin ({units['temp'][alt_unit]})"
        tmax_c = f"tmax ({units['temp'][alt_unit]})"
        srad_wm2 = f"srad ({units['srad'][alt_unit]})"
        dayl_s = "dayl (s)"
        tmean_c = "tmean (deg c)"
        rh = "rh (-)"
        u2 = "u2 (m/s)"

        reqs = [tmin_c, tmax_c, srad_wm2, dayl_s]

        _check_requirements(reqs, clm_df.columns)

        clm_df[tmean_c] = 0.5 * (clm_df[tmax_c] + clm_df[tmin_c])
        delta_v = (
            4098
            * (
                0.6108
                * np.exp(
                    17.27 * clm_df[tmean_c] / (clm_df[tmean_c] + 237.3),
                )
            )
            / ((clm_df[tmean_c] + 237.3) ** 2)
        )
        elevation = py3dep.elevation_bycoords([coords], crs)[0]

        # Atmospheric pressure [kPa]
        pa = 101.3 * ((293.0 - 0.0065 * elevation) / 293.0) ** 5.26
        # Latent Heat of Vaporization [MJ/kg]
        lmbda = 2.501 - 0.002361 * clm_df[tmean_c]
        # Psychrometric constant [kPa/°C]
        gamma = 1.013e-3 * pa / (0.622 * lmbda)

        e_max = 0.6108 * np.exp(17.27 * clm_df[tmax_c] / (clm_df[tmax_c] + 237.3))
        e_min = 0.6108 * np.exp(17.27 * clm_df[tmin_c] / (clm_df[tmin_c] + 237.3))
        e_s = (e_max + e_min) * 0.5
        e_a = clm_df[rh] * e_s * 1e-2 if rh in clm_df else e_min
        e_def = e_s - e_a

        jday = clm_df.index.dayofyear
        r_surf = clm_df[srad_wm2] * clm_df[dayl_s] * 1e-6

        alb = 0.23

        jp = 2.0 * np.pi * jday / 365.0
        d_r = 1.0 + 0.033 * np.cos(jp)
        delta_r = 0.409 * np.sin(jp - 1.39)
        phi = coords[1] * np.pi / 180.0
        w_s = np.arccos(-np.tan(phi) * np.tan(delta_r))
        r_aero = (
            24.0
            * 60.0
            / np.pi
            * 0.082
            * d_r
            * (w_s * np.sin(phi) * np.sin(delta_r) + np.cos(phi) * np.cos(delta_r) * np.sin(w_s))
        )
        rad_s = (0.75 + 2e-5 * elevation) * r_aero
        rad_ns = (1.0 - alb) * r_surf
        rad_nl = (
            4.903e-9
            * (((clm_df[tmax_c] + 273.16) ** 4 + (clm_df[tmin_c] + 273.16) ** 4) * 0.5)
            * (0.34 - 0.14 * np.sqrt(e_a))
            * ((1.35 * r_surf / rad_s) - 0.35)
        )
        rad_n = rad_ns - rad_nl

        # recommended for daily data
        rho_s = 0.0
        # recommended when no data is available
        u_2m = clm_df[u2] if u2 in clm_df else 2.0
        clm_df["pet (mm/day)"] = (
            0.408 * delta_v * (rad_n - rho_s)
            + gamma * 900.0 / (clm_df[tmean_c] + 273.0) * u_2m * e_def
        ) / (delta_v + gamma * (1 + 0.34 * u_2m))

        clm_df = clm_df.drop(columns=tmean_c)
        return clm_df

    @staticmethod
    def pet_bygrid(clm_ds: xr.Dataset) -> xr.Dataset:
        """Compute Potential EvapoTranspiration using Daymet dataset.

        Notes
        -----
        The method is based on
        `FAO Penman-Monteith equation <http://www.fao.org/3/X0490E/x0490e06.htm>`__
        assuming that soil heat flux density is zero.

        Parameters
        ----------
        clm_ds : xarray.DataArray
            The dataset must include at least the following variables:
            ``tmin``, ``tmax``, ``lat``, ``lon``, ``srad``, ``dayl``. Also, if
            ``rh`` (relative humidity) and ``u2`` (wind at 2 m level)
            are available, they are used. Otherwise, actual vapour pressure is assumed
            to be saturation vapour pressure at daily minimum temperature and 2-m wind
            speed is considered to be 2 m/s.

        Returns
        -------
        xarray.DataArray
            The input dataset with an additional variable called ``pet`` in mm/day.
        """
        keys = list(clm_ds.keys())
        reqs = ["tmin", "tmax", "lat", "lon", "srad", "dayl"]

        _check_requirements(reqs, keys)

        dtype = clm_ds.tmin.dtype
        dates = clm_ds["time"]
        clm_ds["tmean"] = 0.5 * (clm_ds["tmax"] + clm_ds["tmin"])

        # Slope of saturation vapour pressure [kPa/°C]
        clm_ds["delta_r"] = (
            4098
            * (0.6108 * np.exp(17.27 * clm_ds["tmean"] / (clm_ds["tmean"] + 237.3)))
            / ((clm_ds["tmean"] + 237.3) ** 2)
        )

        res = clm_ds.res[0] * 1.0e3
        elev = py3dep.elevation_bygrid(clm_ds.x.values, clm_ds.y.values, clm_ds.crs, res)
        clm_ds = xr.merge([clm_ds, elev], combine_attrs="override")
        clm_ds["elevation"] = clm_ds.elevation.where(
            ~np.isnan(clm_ds.isel(time=0)[keys[0]]), drop=True
        ).T

        # Atmospheric pressure [kPa]
        pa = 101.3 * ((293.0 - 0.0065 * clm_ds["elevation"]) / 293.0) ** 5.26
        # Latent Heat of Vaporization [MJ/kg]
        lmbda = 2.501 - 0.002361 * clm_ds["tmean"]
        # Psychrometric constant [kPa/°C]
        clm_ds["gamma"] = 1.013e-3 * pa / (0.622 * lmbda)

        # Saturation vapor pressure [kPa]
        e_max = 0.6108 * np.exp(17.27 * clm_ds["tmax"] / (clm_ds["tmax"] + 237.3))
        e_min = 0.6108 * np.exp(17.27 * clm_ds["tmin"] / (clm_ds["tmin"] + 237.3))
        e_s = (e_max + e_min) * 0.5

        clm_ds["e_a"] = clm_ds["rh"] * e_s * 1e-2 if "rh" in keys else e_min
        clm_ds["e_def"] = e_s - clm_ds["e_a"]

        lat = clm_ds.isel(time=0).lat
        clm_ds["time"] = pd.to_datetime(clm_ds.time.values).dayofyear.astype(dtype)
        r_surf = clm_ds["srad"] * clm_ds["dayl"] * 1e-6

        alb = 0.23

        jp = 2.0 * np.pi * clm_ds["time"] / 365.0
        d_r = 1.0 + 0.033 * np.cos(jp)
        delta_r = 0.409 * np.sin(jp - 1.39)
        phi = lat * np.pi / 180.0
        w_s = np.arccos(-np.tan(phi) * np.tan(delta_r))
        r_aero = (
            24.0
            * 60.0
            / np.pi
            * 0.082
            * d_r
            * (w_s * np.sin(phi) * np.sin(delta_r) + np.cos(phi) * np.cos(delta_r) * np.sin(w_s))
        )
        rad_s = (0.75 + 2e-5 * clm_ds["elevation"]) * r_aero
        rad_ns = (1.0 - alb) * r_surf
        rad_nl = (
            4.903e-9
            * (((clm_ds["tmax"] + 273.16) ** 4 + (clm_ds["tmin"] + 273.16) ** 4) * 0.5)
            * (0.34 - 0.14 * np.sqrt(clm_ds["e_a"]))
            * ((1.35 * r_surf / rad_s) - 0.35)
        )
        clm_ds["rad_n"] = rad_ns - rad_nl

        # recommended for daily data
        rho_s = 0.0
        # recommended when no data is available
        u_2m = clm_ds["u2"] if "u2" in keys else 2.0
        clm_ds["pet"] = (
            0.408 * clm_ds["delta_r"] * (clm_ds["rad_n"] - rho_s)
            + clm_ds["gamma"] * 900.0 / (clm_ds["tmean"] + 273.0) * u_2m * clm_ds["e_def"]
        ) / (clm_ds["delta_r"] + clm_ds["gamma"] * (1 + 0.34 * u_2m))
        clm_ds["pet"].attrs["units"] = "mm/day"

        clm_ds["time"] = dates

        clm_ds = clm_ds.drop_vars(["delta_r", "gamma", "e_def", "rad_n", "tmean", "e_a"])

        return clm_ds


def _check_requirements(reqs: Iterable, cols: List[str]) -> None:
    """Check for all the required data.

    Parameters
    ----------
    reqs : iterable
        A list of required data names (str)
    cols : list
        A list of variable names (str)
    """
    if not isinstance(reqs, Iterable):
        raise InvalidInputType("reqs", "iterable")

    missing = [r for r in reqs if r not in cols]
    if missing:
        raise MissingItems(missing)
