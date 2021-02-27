#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_yaml import read_yaml

file_path = 'config.yaml'
dict_ = read_yaml(file_path)

ENV = dict_['APP']['ENVIRONMENT']

host = dict_['DB_LOCAL']['HOST']
database = dict_['DB_LOCAL']['DATABASE']
user = dict_['DB_LOCAL']['USER']
password = dict_['DB_LOCAL']['PASSWORD']
port = dict_['DB_LOCAL']['PORT']
ECHO = dict_['DB_LOCAL']['ECHO']
LOCAL_DB_STR_CONNECTION = ("mysql+mysqlconnector:"
            f"//{user}:{password}@{host}:{port}/{database}")

host_ = dict_['DB_PROD']['HOST']
database_ = dict_['DB_PROD']['DATABASE']
user_ = dict_['DB_PROD']['USER']
password_ = dict_['DB_PROD']['PASSWORD']
port_ = dict_['DB_PROD']['PORT']
# ECHO = dict_['DB_PROD']['ECHO']
PROD_DB_STR_CONNECTION = ("mysql+mysqlconnector:"
            f"//{user}:{password}@{host}:{port}/{database}")

MAX_TILT = dict_['EVALUATOR']['MAX_TILT']
DELTA_TILT = dict_['EVALUATOR']['DELTA_TILT']
MAX_DELTA_USER_THRP_DL_PERCENTAJE = dict_['EVALUATOR']['MAX_DELTA_USER_THRP_DL_PERCENTAJE']
MAX_DELTA_TRAFFIC_DL_PERCENTAJE = dict_['EVALUATOR']['MAX_DELTA_TRAFFIC_DL_PERCENTAJE']
MIN_USER_AVG = dict_['EVALUATOR']['MIN_USER_AVG']
MAX_USER_AVG = dict_['EVALUATOR']['MAX_USER_AVG']
