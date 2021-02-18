#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
# import numpy as np

from loguru import logger

def get_cells_df():
    logger.info(f'get_cells_df:')
    return pd.read_csv("./data/lcellreference_2020_12_30.csv")

# esta función debe eliminarse y usarse la de abajo
def get_ta_df():
    logger.info(f'get_ta_df:')
    return pd.read_csv("./data/prs_lte_hour_2020_12_30.csv")

def get_prs_lte_hour_df():
    logger.info(f'get_prs_lte_hour_df:')
    return pd.read_csv("./data/prs_lte_hour_2020_12_30.csv")

def get_period_data(period = None):
    logger.info(f'get_period_data:')
    return pd.read_json (f'./data/_prs_lte_hour_{period}.json')

def get_ret_data(period = None):
    logger.info(f'get_ret_data:')
    return pd.read_json (f'./data/ret_data_{period}.json')

def get_ret_join_data(period = None):
    logger.info(f'get_ret_data:')
    return pd.read_json (f'./data/ret_join_data_{period}.json')
