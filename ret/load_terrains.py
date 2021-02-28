#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
# import numpy as np
import pandas as pd

from loguru import logger

from terrains_data import terrains_data

from settings import (
        ENV,
    )

from tables import (
        get_engine,
        get_session,
    )

def load_terrains(time_=None):
    logger.info(f'ENV {ENV}')

    if not time_:
        return

    list_ = [
                {
                    'datetimeid' : time_,
                    'cellname' : 'AIS_4G_003_3',
                    'is_plain' : True,
                    'slope' : 0,
                },
                {
                    'datetimeid' : time_,
                    'cellname' : 'ARA_4G_013_3',
                    'is_plain' : True,
                    'slope' : 0,
                },
            ]

    if ENV == 'sim':
        df = pd.DataFrame.from_dict(list_)

    if ENV == 'prod':
        df = terrains_data(time_=time_)

    logger.info(f'df.shape {df.shape}')

    engine = get_engine()
    session = get_session(engine=engine)
    df.to_sql('terrains', con=engine, if_exists='append', index=False)
    session.commit()
    session.close()

if __name__ == '__main__':
    load_terrains(time_=datetime.datetime(2021, 1, 10, 10, 30, 0, 0))

