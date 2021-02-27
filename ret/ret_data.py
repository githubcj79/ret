#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import mysql.connector
import pandas as pd
from loguru import logger
from mysql.connector import errorcode
# from mysql.connector.cursor import MySQLCursor

from settings import (
        ENV,
        host_,
        database_,
        user_,
        password_,
        port_,
    )

def ret_data(time_=None):
    logger.debug(f'ENV {ENV}')

    if not time_:
        logger.info(f'ENV {ENV}')
        return

    # now_ = datetime.datetime.now()
    # day_before = time_  - datetime.timedelta(days=1)
    now_ = time_
    period = now_.strftime("%Y-%m-%d")

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
    and (x.deviceno = y.localcellid or x.deviceno = y.localcellid + 10)
    and STR_TO_DATE(y.dateid, '%Y-%m-%d') = '{period}');
    '''

    try:

        cnx = mysql.connector.connect(
                user=user_,
                password=password_,
                host=host_,
                database=database_,
                use_pure=True,
            )

        query = query_
        df = pd.read_sql(query,cnx)
        cnx.close()
        return df

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logger.error("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logger.error("Database does not exist")
      else:
        logger.error(err)
    else:
      cnx.close()

def main():
        df = ret_data(time_=datetime.datetime(2021, 2, 25, 10, 30, 0, 0))


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
