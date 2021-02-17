#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
import pandas as pd

def mid_term_evaluator(time_=None, candidates_df=pd.DataFrame()):
    if not time_:
        return

    logger.debug(f"time_ {time_}")

    if candidates_df.empty:
        return
