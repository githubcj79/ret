#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from loguru import logger
from sqlalchemy import and_

import pandas as pd

from tables import (
        Ret,
        Transaction,
        get_engine,
        get_session,
    )

def newtilt(tilt=None):
    logger.debug(f"tilt {tilt}")

    if not tilt:
        return

    max_tilt = 50
    delta_tilt = 1
    return tilt + delta_tilt if tilt + delta_tilt < max_tilt else tilt

def delta_percentaje(reference=None, value=None):
    logger.debug(f"reference {reference} value {value}")

    if not reference or not value:
        return

    delta = reference - value
    return delta * 100 / reference

def evaluator(time_=None, candidates_kpis_df=pd.DataFrame()):
    '''
    Esta función recibe todas las celdas candidatas y sus kpis promedio,
    para el instante actual.
    Dependiendo de si la celda existe en la tabla transactions,
    hay comparaciones con kpis promedio iniciales.
    En base a reglas pueden entrar transacciones a la tabla transactions.
    '''
    logger.debug(f"time_ {time_}")

    if not time_:
        return

    if candidates_kpis_df.empty:
        return

    logger.debug(f"candidates_kpis_df \n{candidates_kpis_df}")

    engine = get_engine()
    session = get_session(engine=engine)

    for idx in candidates_kpis_df.index: # overshooters plain terrain
        node = candidates_kpis_df['eNodeB_Name'][idx]
        user_avg = candidates_kpis_df['user_avg'][idx]
        user_thrp_dl = candidates_kpis_df['user_thrp_dl'][idx]
        traffic_dl = candidates_kpis_df['traffic_dl'][idx]

        antennas = session.query(Ret).filter(Ret.node==node,)
        for antenna in antennas:
            logger.info(f"node {antenna.node} deviceno {antenna.deviceno}")
            trx = session.query(Transaction).filter(
                and_(Transaction.node==antenna.node,
                    Transaction.deviceno==antenna.deviceno)).first()
            if trx:
                # si trx anterior no fue exitosa
                if not trx.success:
                    logger.info(f"continue: success {trx.success}")
                    continue
                cond_ = delta_percentaje(
                    trx.user_thrp_dl_initial, user_thrp_dl) > 5.0
                cond_ = cond_ or delta_percentaje(
                        trx.traffic_dl_initial, traffic_dl) > 10.0
                if cond_:
                    # rollback
                    logger.info(f"rollback")
                    newtilt_  = trx.oldtilt
                else:
                    newtilt_ = newtilt(trx.newtilt)

                if trx.newtilt == newtilt_:
                    logger.info(f"continue: newtilt_ {newtilt_}")
                    continue

                # si nuevo tilt es distinto al último
                trx.newtilt = newtilt_
                trx.generated = datetime.now()
            else:
                if not (user_avg >= 80.0 and user_avg <= 200.0):
                    logger.info(f"continue: user_avg {user_avg}")
                    continue
                # se crea entrada en tabla transactions
                trx = Transaction(
                        node = antenna.node,
                        cellname = antenna.cellname,
                        deviceno = antenna.deviceno,
                        subunitno = antenna.subunitno,
                        tilt_initial = antenna.tilt,
                        user_thrp_dl_initial = user_thrp_dl,
                        traffic_dl_initial = traffic_dl,
                        newtilt = newtilt(antenna.tilt),
                        datetimeid = time_,
                        generated = datetime.now(),
                        )
                logger.info(f"trx \n{trx}")
                session.add(trx)
            session.commit()

    session.commit()
    session.close()
