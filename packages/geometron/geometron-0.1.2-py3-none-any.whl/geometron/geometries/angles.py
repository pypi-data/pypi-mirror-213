import numpy as np


# from shapely.geometry import Point

def dd_mmsss_to_dd(x):
    """
    Converts angle expressed as degrees.minutesseconds (DDD.MMSSS) to decimal degrees (DDD.XXX)

    Parameters
    ----------
    x : float
         angle in degrees minute

    Returns
    -------
    angle : float
            angle converted to the decimal degrees format
    """

    degrees = np.floor(x)
    minutes = (x - degrees) * 100
    seconds = (minutes - np.floor(minutes)) * 100
    minutes = np.floor(minutes)
    print(degrees, minutes, seconds)
    return degrees + minutes / 60 + seconds / 3600


def ddmm_to_dd(x):
    """
    Converts angle expressed as degrees minutes (DDDMM) to decimal degrees (DDD.XXX)

    Parameters
    ----------
    x : float
         angle in degrees minute

    Returns
    -------
    angle : float
            angle converted to the decimal degrees format
    """

    degrees = float(x) // 100
    minutes = x - 100. * degrees
    return degrees + minutes / 60.


def dd_to_ddmmss(x, string_output=True, precision=3):
    """
        Converts angle expressed as decimal degrees (DD) to minutes (DDMMSS)

        Parameters
        ----------
        x : float
             angle in decimal degrees

        str: bool
            True if output is a string

        precision: int, default : 3
            number of decimals retained for seconds in string output

        Returns
        -------
        angle : string_output
                angle converted to the degrees minutes seconds format
        """

    degrees = np.floor(x)
    decimals = x - degrees
    minutes = decimals * 60
    seconds = (minutes - np.floor(minutes)) * 60
    if string_output:
        return f'{int(degrees):02d}°{int(np.floor(minutes)):02d}\'{seconds:02.{precision}f}"'
    else:
        return int(degrees), int(np.floor(minutes)), seconds


def azimuth(origin, target):
    """
    Computes the Azimuth of a target point as seen from a origin point in a planar coordinate system

    Parameters
    ----------
    origin : shapely.geometry.Point
             Point from which the target is observed

    target : shapely.geometry.Point
             Point which is observed from the origin
    Returns
    -------
    azimuth: `float`
             azimuth angle in radians

    """

    az = np.arctan2(target.coords[0][0] - origin.coords[0][0], target.coords[0][1] - origin.coords[0][1])
    az = np.fmod(az + 2 * np.pi, 2 * np.pi)
    return az
