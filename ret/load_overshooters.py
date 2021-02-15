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

def load_overshooters(period=None):
    logger.info(f'load_overshooters:')

    if not period:
        return

    list_ = [
                {
                    'datetimeid' : period,
                    'cellname' : 'AIS_4G_003_3',
                    'ta_calculated' : 14.4,
                    'average_distance' : 2.43982546537283,
                    'overshooter' : True,
                    'intensity' : 'High',
                },
                {
                    'datetimeid' : period,
                    'cellname' : 'ARA_4G_013_3',
                    'ta_calculated' : 14.4,
                    'average_distance' : 6.14587256200947,
                    'overshooter' : True,
                    'intensity' : 'High',
                },
            ]

    engine = get_engine()
    session = get_session(engine=engine)

    df = pd.DataFrame.from_dict(list_)
    df.to_sql('overshooters', con=engine, if_exists='append', index=False)

    session.commit()
    session.close()


if __name__ == '__main__':
    load_overshooters(period=datetime.datetime(2021, 1, 10, 10, 30, 0, 0))

