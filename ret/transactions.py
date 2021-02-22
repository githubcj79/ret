#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import null
from loguru import logger
import pandas as pd

from giver_of_times import giver_of_times

from tables import (
        Ret,
        Transaction,
        get_engine,
        get_session,
    )

def transactions(time_=None):
    '''
    Esta función detecta las transacciones en la tabla transactions.
    y las ejecuta sobre el nbi.
    Por ahora no se reintentan transacciones fallidas.
    '''
    logger.debug(f"time_ {time_}")

    engine = get_engine()
    session = get_session(engine=engine)
    # ----------------------------------------
    # detectar las transacciones a procesar
    trxs = session.query(Transaction).filter(Transaction.sent.is_(null()))
    for trx in trxs:
        logger.info(f"trx \n{trx}")
    # ----------------------------------------
    session.commit()
    session.close()

    if not time_:
        return

def main():
    for time_ in giver_of_times():
        transactions(time_)


if __name__ == '__main__':
    main()
