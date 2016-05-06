# -*- coding: utf-8 -*-

"""
This module contains formulas for calculating PV power.
"""

import pvlib
import pandas as pd


def f_ac_power(inverter, v_mp, p_mp):
    """
    Calculate AC power

    :param inverter:
    :param v_mp:
    :param p_mp:
    :return: AC power [W]
    """
    return pvlib.pvsystem.snlinverter(inverter, v_mp, p_mp).values


def f_dc_power(times, module, poa_direct, poa_diffuse, cell_temp, am_abs, aoi):
    """
    Calculate DC power

    :param times: timestamps
    :param module: PV module dictionary or pandas data frame
    :param poa_direct: plane of array direct irradiance [W/m**2]
    :param poa_diffuse: plane of array diffuse irradiance [W/m**2]
    :param cell_temp: PV cell temperature [degC]
    :param am_abs: absolute air mass [dimensionless]
    :param aoi: angle of incidence [degrees]
    :return: short circuit current (Isc) [A], max. power current (Imp) [A],
        open circuit voltage (Voc) [V], max. power voltage (Vmp) [V],
        max. power (Pmp) [W], effective irradiance (Ee) [suns]
    """
    poa_direct = pd.Series(poa_direct, index=times)
    poa_diffuse = pd.Series(poa_diffuse, index=times)
    cell_temp = pd.Series(cell_temp, index=times)
    am_abs = pd.Series(am_abs, index=times)
    aoi = pd.Series(aoi, index=times)
    dc = pvlib.pvsystem.sapm(
        module, poa_direct, poa_diffuse, cell_temp, am_abs, aoi
    )
    fields = ('i_sc', 'i_mp', 'v_oc', 'v_mp', 'p_mp', 'effective_irradiance')
    return tuple(dc[field].values for field in fields)


def f_cell_temp(poa_global, wind_speed, air_temp):
    """
    Calculate cell temperature.

    :param poa_global: plane of array global irradiance [W/m**2]
    :param wind_speed: wind speed [m/s]
    :param air_temp: ambient dry bulb air temperature [degC]
    :return: cell temperature [degC]
    """
    temps = pvlib.pvsystem.sapm_celltemp(poa_global, wind_speed, air_temp)
    return temps['temp_cell'].values, temps['temp_module'].values


def f_aoi(surface_tilt, surface_azimuth, solar_zenith, solar_azimuth):
    """
    Calculate angle of incidence

    :param surface_tilt:
    :param surface_azimuth:
    :param solar_zenith:
    :param solar_azimuth:
    :return: angle of incidence [deg]
    """
    return pvlib.irradiance.aoi(surface_tilt, surface_azimuth,
                                solar_zenith, solar_azimuth)