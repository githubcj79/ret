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

def load_rets(period=None):
    logger.info(f'load_rets:')

    if not period:
        return

    list_ = [
                {
                    'datetimeid' : period,
                    'node' : 'MBTS-AIS_3G_003',
                    'cellname' : 'AIS_4G_003_3',
                    'eci' : 2816002,
                    'devicename' : 'RET82',
                    'deviceno' : 2,
                    'tilt' : 30,
                    'subname' : 'RET82',
                    'subunitno' : 1,
                    'localcellid' : 2,
                },
                {
                    'datetimeid' : period,
                    'node' : 'MBTS-ARA_3G_013',
                    'cellname' : 'ARA_4G_013_3',
                    'eci' : 2304258,
                    'devicename' : 'RET82R_S3',
                    'deviceno' : 2,
                    'tilt' : 40,
                    'subname' : 'RET82R_S3',
                    'subunitno' : 1,
                    'localcellid' : 2,
                },
                {
                    'datetimeid' : period,
                    'node' : 'MBTS-ARA_3G_013',
                    'cellname' : 'ARA_4G_013_3',
                    'eci' : 2304258,
                    'devicename' : 'RET82L_S3',
                    'deviceno' : 12,
                    'tilt' : 40,
                    'subname' : 'RET82L_S3',
                    'subunitno' : 1,
                    'localcellid' : 2,
                },
            ]

    engine = get_engine()
    session = get_session(engine=engine)

    df = pd.DataFrame.from_dict(list_)
    df.to_sql('rets', con=engine, if_exists='append', index=False)

    session.commit()
    session.close()


if __name__ == '__main__':
    load_rets(period=datetime.datetime(2021, 1, 10, 10, 30, 0, 0))

