#!/usr/bin/env python
"""
Script to download publicly available TEC maps from
https://cddis.nasa.gov/archive/gps/products/ionex/yyyy/ddd/

Version history:
v0.1 modified from ftpdownload.py, Charlotte Sobey 2021
v0.2 updated for new file naming scheme and added date range option, C. P. Lee 2023
"""

from datetime import datetime, timedelta
import argparse
import requests


def get_date_range(start_date, end_date):
    """
    Find every date in the given range.

    Parameters
    ----------
    start_date : datetime
        An instance of the datetime class containing the start date.
    end_date : datetime
        An instance of the datetime class containing the end date.

    Returns
    -------
    date_range : list
        A list of datetime objects containing the dates in the given range.
    """
    current_date = start_date
    date_range = []
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    return date_range


def format_ionex_short(date, ionex_type):
    """
    Format the IONEX filename using the short naming convention.

    Parameters
    ----------
    date : datetime
        An instance of the datetime class containing the date of the file.
    ionex_type : str
        The IONEX type of the file.

    Returns
    -------
    filename : str
        The IONEX filename in the old format.
        e.g. igsgddd0.yyi.Z
    """
    dayofyear = date.timetuple().tm_yday
    filename = f'{ionex_type}{dayofyear:03d}0.{date.strftime("%y")}i.Z'
    return filename


def format_ionex_long(date, ionex_type):
    """
    Format the IONEX filename using the long naming convention.
    For details, see: https://igs.org/products/#ionosphere


    Parameters
    ----------
    date : datetime
        An instance of the datetime class containing the date of the file.
    ionex_type : str
        The IONEX type of the file.

    Returns
    -------
    filename : str
        The IONEX filename in the new format
        e.g. IGS0OPSFIN_yyyyddd0000_01D_02H_GIM.INX.gz
    """
    dayofyear = int(date.timetuple().tm_yday)
    year = int(date.strftime("%Y"))
    filename = None
    if ionex_type == "igsg":
        if year > 2022:
            filename = f"IGS0OPSFIN_{year}{dayofyear:03d}0000_01D_02H_GIM.INX.gz"
    elif ionex_type == "codg":
        if year == 2022 and dayofyear > 330 or year > 2022:
            filename = f"COD0OPSFIN_{year}{dayofyear:03d}0000_01D_01H_GIM.INX.gz"
    elif ionex_type == "esag":
        if year == 2022 and dayofyear > 330 or year > 2022:
            filename = f"ESA0OPSFIN_{year}{dayofyear:03d}0000_01D_02H_ION.IOX.gz"
    elif ionex_type == "jplg":
        if year == 2023 and dayofyear == 212:
            filename = f"JPL0OPSFIN_{year}{dayofyear:03d}0000_01D_02H_GIM.INX.gz"
        elif year == 2023 and dayofyear > 218 or year > 2023:
            filename = f"JPL0OPSFIN_{year}{dayofyear:03d}0000_01D_02H_GIM.INX.gz"
    return filename


def main():
    types = ["igsg", "jplg", "codg", "casg", "upcg", "uqrg"]
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--date", type=str, help="Date in YYYY-MM-DD", required=True)
    parser.add_argument(
        "-e",
        "--end_date",
        type=str,
        help="End of date range in YYYY-MM-DD. Will treat the -d option as the start date.",
    )
    parser.add_argument("-t", "--type", type=str, choices=types, default="codg", help="IONEX type")
    args = parser.parse_args()

    # Parse the date or date range
    try:
        start_date = datetime.strptime(args.date, "%Y-%m-%d")
    except:
        parser.error(f"Date format not recognised: {args.date}")
    if not args.end_date:
        dates = [start_date]
    else:
        try:
            end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
        except:
            parser.error(f"Date format not recognised: {args.end_date}")
        dates = get_date_range(start_date, end_date)

    for date in dates:
        short_filename = format_ionex_short(date, args.type)
        long_filename = format_ionex_long(date, args.type)
        dayofyear = int(date.timetuple().tm_yday)
        year = int(date.strftime("%Y"))
        if long_filename is None:
            url = f"https://cddis.nasa.gov/archive/gps/products/ionex/{year}/{dayofyear:03d}/{short_filename}"
        else:
            url = f"https://cddis.nasa.gov/archive/gps/products/ionex/{year}/{dayofyear:03d}/{long_filename}"

        print(f"Requesting URL: {url}")
        r = requests.get(url)

        print(f"Saving file as: {short_filename}")
        with open(short_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1000):
                f.write(chunk)


if __name__ == "__main__":
    main()
