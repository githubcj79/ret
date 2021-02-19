#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
import pandas as pd

def evaluator(time_=None, candidates_kpis_df=pd.DataFrame()):
    '''
    Esta función decide modificaciones a los tilts de algunas antenas en base al momento en el tiempo y data.
    Lo anterior se refleja en modificaciones a la tabla transactions.
    La data es un dataframe con las celdas candidatas e información sobre promedios de kpis en ese periodo.Las columnas son: cellname, user_avg, user_thrp_dl, traffic_dl.
    '''
    logger.debug(f"time_ {time_}")

    if not time_:
        return

    if candidates_kpis_df.empty:
        return

    logger.debug(f"candidates_kpis_df \n{candidates_kpis_df}")

    for idx in candidates_kpis_df.index:
        logger.debug(f"cellname {candidates_kpis_df['cellname'][idx]}")

        # ------------- rule -------------
        user_avg = candidates_kpis_df['user_avg'][idx]
        if not (user_avg > 80 and user_avg < 200  ): # rule
            logger.info(f"rechazado: user_avg {user_avg}")
            continue
        logger.info(f"aceptado: user_avg {user_avg}")

        # ------------- rule -------------


    # si cumple las condiciones y NO EXISTE en la tabla transactions
    # debe entrar a la tabla y registrarse allí los valores iniciales
    # de los kpi para hacer las comparaciones posteriores.

    # Idea Evaluator(time_, cellname) # decide si escribe en la tab transactions,
