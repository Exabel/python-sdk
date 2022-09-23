"""
This file is here to keep backwards capability with the old name of the time series import script.
"""
import sys

from exabel_data_sdk.scripts.load_time_series_from_file import LoadTimeSeriesFromFile

if __name__ == "__main__":
    LoadTimeSeriesFromFile(sys.argv).run()
