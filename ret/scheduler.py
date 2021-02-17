#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
import pandas as pd

from giver_of_times import giver_of_times

from tables import (
        get_engine,
    )

def scheduler(time_=None):
    if not time_:
        return

    logger.debug(f"time_ {time_}")

    engine = get_engine()
    db_connection = engine.connect()

    # set más reciente de overshooters en terreno plano
    query_ = '''
            select o.cellname
            from overshooters o, terrains t
            where o.cellname = t.cellname
                and o.overshooter and t.is_plain
                and o.datetimeid = (select max(datetimeid) from overshooters)
                and t.datetimeid = (select max(datetimeid) from terrains);
            '''

    df = pd.read_sql(query_, db_connection)
    db_connection.close()

    # entregar los candidatos a mid_term_evaluator()

    return df

def main():
    for time_ in giver_of_times():
        scheduler(time_)


if __name__ == '__main__':
    main()
