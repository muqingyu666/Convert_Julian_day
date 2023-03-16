#                  ___====-_  _-====___
#            _--^^^#####//      \\#####^^^--_
#         _-^##########// (    ) \\##########^-_
#        -############//  |\^^/|  \\############-
#      _/############//   (@::@)   \\############\_
#     /#############((     \\//     ))#############\
#    -###############\\    (oo)    //###############-
#   -#################\\  / VV \  //#################-
#  -###################\\/      \//###################-
# _#/|##########/\######(   /\   )######/\##########|\#_
# |/ |#/\#/\#/\/  \#/\##\  |  |  /##/\#/  \/\#/\#/\#| \|
# `  |/  V  V  `   V  \#\| |  | |/#/  V   '  V  V  \|  '
#    `   `  `      `   / | |  | | \   '      '  '   '
#                     (  | |  | |  )
#                    __\ | |  | | /__
#                   (vvv(VVV)(VVV)vvv)
#                       神兽保佑
#                      代码无BUG!
"""

    Code to convert julian day to actual date time 64 format.
        
    Owner: Mu Qingyu
    version 1.0
        version 1.1: 2023-03-16
          
    Created: 2022-05-19
    
    Including the following parts:

        1) Module decimal_to_sexagesimal: Convert decimal time to actual minutes
        
        2) Module decimal_to_time: Convert decimal time to actual time main function
        
        3) Module juliandate_to_utc: Convert julian day to actual date time 64 format
        
"""

import datetime
import math

import numpy as np

###################################################################################
################### Convert Julian day ############################################
###################################################################################

class JulianDay:
    def __init__(self, julian_day: int):
        """Create a new instance of the class.

        Args:
            julian_day (int): The Julian day to create.
        """
        self.julian_day = julian_day

    def _decimal_to_sexagesimal(self, decimal: float) -> tuple:
        """
        Convert decimal hours or degrees to sexagesimal.

        Args:
            decimal (float): Decimal number to be converted to sexagesimal.

        Returns:
            tuple: (hours, minutes, seconds) or (degrees, arcminutes, arcseconds)
        """
        fractional, integral = np.modf(decimal)
        min_fractional, minutes = np.modf(fractional * 60)
        seconds = min_fractional * 60.0

        return int(integral), int(minutes), seconds

    def _decimal_to_time(self, hours: float) -> datetime.time:
        """
        Convert decimal time to a time object.

        Args:
            hours (float): Input time.

        Returns:
            datetime.time: Time object.
        """
        hours, minutes, seconds = self._decimal_to_sexagesimal(hours)
        seconds_frac, seconds = math.modf(seconds)
        seconds = int(seconds)
        microseconds = int(seconds_frac * 1e6)

        return datetime.time(hours, minutes, seconds, microseconds)

    def juliandate_to_utc(self) -> datetime.datetime:
        """
        Convert Julian Date to datetime object in UTC.

        Returns:
            datetime.datetime: Datetime object in UTC time.
        """
        # increment by 0.5
        julian_day = self.julian_day + 0.5
        # split into integer and fractional parts
        jd_frac, jd_int = math.modf(julian_day)

        if jd_int > 2299160:
            a = int((jd_int - 1867216.25) / 36524.25)
            b = jd_int + 1 + a - int(a / 4)
        else:
            b = jd_int
        c = b + 1524
        d = int((c - 122.1) / 365.25)
        e = int(365.25 * d)
        g = int((c - e) / 30.6001)

        day = c - e + jd_frac - int(30.6001 * g)

        if g < 13.5:
            month = g - 1
        else:
            month = g - 13
        month = int(month)

        if month > 2.5:
            year = d - 4716
        else:
            year = d - 4715
        year = int(year)

        day_frac, day = math.modf(day)

        day = int(day)
        date = datetime.date(year, month, day)
        # fractional part of day * 24 hours
        hours = day_frac * 24

        time = self._decimal_to_time(hours)

        return datetime.datetime.combine(date, time)


if __name__ == "__main__":
    pass