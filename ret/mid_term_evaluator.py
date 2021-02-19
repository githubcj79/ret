#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
import pandas as pd

from average_kpis import average_kpis
from evaluator import evaluator

def mid_term_evaluator(time_=None, candidates_df=pd.DataFrame()):
    logger.debug(f"time_ {time_}")

    if not time_:
        return

    if candidates_df.empty:
        return

    kpis_df = average_kpis(time_)
    if kpis_df.empty:
        return

    l = ['cellname', 'user_avg', 'user_thrp_dl', 'traffic_dl',]
    candidates_kpis_df = pd.merge(candidates_df, kpis_df, how="inner", left_on='cellname', right_on='cellname')[l].drop_duplicates()

    evaluator(time_=time_, candidates_kpis_df=candidates_kpis_df)

    # Idea Executor < -- > NBI : podría ser un proceso independiente
    # - tengo q revisar q retorna el NBI
    # actualiza tablas transactions y rets
