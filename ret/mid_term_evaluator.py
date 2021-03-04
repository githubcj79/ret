#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from loguru import logger
import pandas as pd

from average_kpis import average_kpis
from evaluator import evaluator
from transactions import transactions

def mid_term_evaluator(time_=None, candidates_df=pd.DataFrame()):
    logger.debug(f"time_ {time_}")

    if not time_:
        return

    if candidates_df.empty:
        return

    day_before = time_  - datetime.timedelta(days=1)
    when_ = day_before
    kpis_df = average_kpis(when_)
    if kpis_df.empty:
        return

    l = ['eNodeB_Name', 'cellname', 'user_avg', 'user_thrp_dl', 'traffic_dl',]
    candidates_kpis_df = pd.merge(candidates_df, kpis_df, how="inner", left_on='cellname', right_on='Cell_Name')[l].drop_duplicates()

    evaluator(time_=time_, candidates_kpis_df=candidates_kpis_df)

    # Idea Executor < -- > NBI : podría ser un proceso independiente
    # - tengo q revisar q retorna el NBI
    # actualiza tablas transactions y rets (nuevo tilt)

    transactions(time_=time_)
