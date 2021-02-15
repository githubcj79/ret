#!/usr/bin/env python
# -*- coding: utf-8 -*-

from read_yaml import read_yaml

file_path = 'config.yaml'
dict_ = read_yaml(file_path)

ENV = dict_['APP']['ENVIRONMENT']

# section = 'mysql_' + ENV
host = dict_['DATABASE']['HOST']
user = dict_['DATABASE']['USERNAME']
password = dict_['DATABASE']['PASSWORD']
database = dict_['DATABASE']['DB']
port = dict_['DATABASE']['PORT']
ECHO = dict_['DATABASE']['ECHO']
# ECHO = config_dict[section]['echo'] == 'True'
DB_STR_CONNECTION = ("mysql+mysqlconnector:"
            f"//{user}:{password}@{host}:{port}/{database}")
