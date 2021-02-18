#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
import pandas as pd

from giver_of_times import giver_of_times
from input_data import get_period_data
from settings import (
        ENV,
    )

import datetime
import time

def average_kpis(time_=None):
    logger.debug(f"ENV {ENV} time_ {time_}")

    if not time_:
        return

    period = time_.strftime("%Y%m%d")
    logger.debug(f"period {period}")

    data_df = pd.DataFrame() # empty df
    if ENV == 'sim':
        dict_ = {
                    'cellname': ['AIS_4G_003_3', 'ARA_4G_013_3',],
                    'user_avg': [81.0, 200.0,],
                    'user_thrp_dl': [25.4, 23.2,],
                    'traffic_dl': [8285.170, 7660.760],
                }
        data_df = pd.DataFrame.from_dict(dict_)
    elif ENV == 'dev':
        data_df = get_period_data(period = period)

    return data_df

def main():
    for time_ in giver_of_times():
        dict_ = average_kpis(time_)
        logger.debug(f"dict_ \n{dict_}")


if __name__ == '__main__':
    main()
