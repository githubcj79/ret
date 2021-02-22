#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_yaml import read_yaml

file_path = 'config.yaml'
dict_ = read_yaml(file_path)

ENV = dict_['APP']['ENVIRONMENT']

host = dict_['DATABASE']['HOST']
user = dict_['DATABASE']['USERNAME']
password = dict_['DATABASE']['PASSWORD']
database = dict_['DATABASE']['DB']
port = dict_['DATABASE']['PORT']
ECHO = dict_['DATABASE']['ECHO']
DB_STR_CONNECTION = ("mysql+mysqlconnector:"
            f"//{user}:{password}@{host}:{port}/{database}")

MAX_TILT = dict_['EVALUATOR']['MAX_TILT']
DELTA_TILT = dict_['EVALUATOR']['DELTA_TILT']
MAX_DELTA_USER_THRP_DL_PERCENTAJE = dict_['EVALUATOR']['MAX_DELTA_USER_THRP_DL_PERCENTAJE']
MAX_DELTA_TRAFFIC_DL_PERCENTAJE = dict_['EVALUATOR']['MAX_DELTA_TRAFFIC_DL_PERCENTAJE']
MIN_USER_AVG = dict_['EVALUATOR']['MIN_USER_AVG']
MAX_USER_AVG = dict_['EVALUATOR']['MAX_USER_AVG']
