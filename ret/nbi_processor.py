#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger

import datetime
import time

from settings import ENV

def nbi_processor(time_=None,session_=None,trxs_=None):
    '''
    Esta función recibe el query (trxs_) con todas las transacciones
    a ejecutar.
    Construye un mensaje al NBI con todas ellas.
    Espera el mensaje de respuesta y de acuerdo con lo recibido
    actualiza las transacciones en la BD (transactions y rets)
    '''
    logger.debug(f"time_ {time_} ENV {ENV}")

    if not time_ or not session_ or not trxs_:
        return

    # logger.debug(f"hello !!! ..")

    for trx in trxs_:
        logger.info(f"trx \n{trx}")
