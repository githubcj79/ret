#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import configparser
# from decouple import config
from sqlalchemy import create_engine
import datetime
import pandas as pd
import pymysql

from settings import (
        ENV,
        PROD_DB_STR_CONNECTION,
    )

from tables import (
        get_engine,
        get_session,
    )

# ENV = config('ENV')
# MYSQL_CONF = config('MYSQL_CONF')

def ret_data(time_=time_):
    logger.debug(f'ENV {ENV}')

    if not time_:
        return

    # global DB_STR_CONNECTION

    # section = 'mysql_' + ENV
    # config_dict = configparser.ConfigParser()
    # config_dict.read(MYSQL_CONF)

    # host = config_dict[section]['host']
    # user = config_dict[section]['user']
    # password = config_dict[section]['password']
    # database = config_dict[section]['database']
    # port = config_dict[section]['port']

    # db_str_connection = ("mysql+pymysql:"
    #                     f"//{user}:{password}@{host}:{port}/{database}")
    # sql_engine = create_engine(db_str_connection, pool_recycle=3600)

    engine = get_prod_engine()
    db_connection = engine.connect()

    day_before = time_  - datetime.timedelta(days=1)
    period = day_before.strftime("%Y-%m-%d")
    logger.info(f'period {period}')

    query_ = f'''
    select x.dateid, x.node, x.devicename, x.deviceno, x.tilt,
    x.subname, x.subunitno, y.localcellid, y.eci, y.cellname
    from (select
    ret.dateid as dateid,
    ret.node as node,
    ret.devicename as devicename,
    ret.deviceno as deviceno,
    sub.tilt as tilt,
    sub.subname as subname,
    sub.subunitno as subunitno
    from ret
    inner join retsubunit sub on
    date(ret.dateid) = date(sub.dateid) and
    ret.node = sub.node and
    ret.deviceno = sub.deviceno
    where date(ret.dateid) = current_date) as x
    inner join lcellreference as y
    on (x.node = y.node
-- and y.node = 'MBTS-RM_3G_048'
    and (x.deviceno = y.localcellid or x.deviceno = y.localcellid + 10)
    and STR_TO_DATE(y.dateid, '%Y-%m-%d') = '{period}');
-- and STR_TO_DATE(y.dateid, '%Y-%m-%d') = '2021-02-08');
    '''

    df = pd.read_sql(query_, db_connection)
    db_connection.close()
    return df

    # -------------------------------------
    # path = r"C:\cygwin64\home\carlos\lab\pandas-mysql\data\ret_adata_20210201.json"
    # df.to_json(path,orient='records')

    # table: prs_lte_hour
    # select * from prs_lte_hour where (dateid_date between '2020-12-02' and '2020-12-02') and dateid_hour = '20';

    # select * from prs_lte_hour where dateid_date = '2021-01-13' and dateid_hour >= '15';

    # query_ = ("select * from prs_lte_hour where "
    #     "(dateid_date between '2020-12-02' "
    #     "and '202-12-02') and dateid_hour = '20' ")

    # for day in ['13', '12', '11', '10']:

    # for day in ['10']:

    #     query_ = f"select * from prs_lte_hour where dateid_date = '2021-01-{day}' and dateid_hour >= '15' "

    #     df = pd.read_sql(query_, db_connection);
    #     pd.set_option('display.expand_df_repr', False)
    #     # print(df)
    #     db_connection.close()

    #     path = r"C:\cygwin64\home\carlos\lab\pandas-mysql\data\_prs_lte_hour_202101" + f'{day}.json'

    #     df.to_json(path,orient='records')
    # -------------------------------------

def main():
        df = ret_data(time_==datetime.datetime(2021, 2, 25, 10, 30, 0, 0))


if __name__ == '__main__':
    main()

'''
/*
This query uses a subquery in the FROM clause.
The subquery is given an alias x so that we can
refer to it in the outer select statement.
*/
select x.ProductID,
    y.ProductName,
    x.max_unit_price
from
(
    select ProductID, max(UnitPrice) as max_unit_price
    from order_details
    group by ProductID
) as x
inner join products as y on x.ProductID = y.ProductID
'''
