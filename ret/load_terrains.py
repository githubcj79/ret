#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import numpy as np
import pandas as pd

from loguru import logger

from tables import (
        get_engine,
        get_session,
    )

def load_terrains(period=None):
    logger.info(f'load_terrains:')

    if not period:
        return

    list_ = [
                {
                    'datetimeid' : period,
                    'cellname' : 'AIS_4G_003_3',
                    'is_plain' : True,
                    'slope' : 0,
                },
                {
                    'datetimeid' : period,
                    'cellname' : 'ARA_4G_013_3',
                    'is_plain' : True,
                    'slope' : 0,
                },
            ]

    engine = get_engine()
    session = get_session(engine=engine)

    df = pd.DataFrame.from_dict(list_)
    df.to_sql('terrains', con=engine, if_exists='append', index=False)

    session.commit()
    session.close()


if __name__ == '__main__':
    load_terrains(period=datetime.datetime(2021, 1, 10, 10, 30, 0, 0))

