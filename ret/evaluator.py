#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
import pandas as pd

def evaluator(time_=None, candidates_kpis_df=pd.DataFrame()):
    logger.debug(f"time_ {time_}")

    if not time_:
        return

    if candidates_kpis_df.empty:
        return

    logger.debug(f"candidates_kpis_df \n{candidates_kpis_df}")

    for idx in candidates_kpis_df.index:
        logger.debug(f"cellname {candidates_kpis_df['cellname'][idx]}")
