#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
import pandas as pd

def mid_term_evaluator(time_=None, candidates_df=pd.DataFrame()):
    if not time_:
        return

    logger.debug(f"time_ {time_}")

    if candidates_df.empty:
        return

    # para cada uno de estos candidatos <---> cellname
    # hay que solicitar:
    # user_avg
    # user_thrp_dl
    # traffic_dl


    # los datos anteriores corresponden al promedio de los valores
    # de esas muestras para la data del periodo actual por celda

    # La idea es invocar una función que devuelva la data anterior para todas
    # las celdas en forma de un data frame <-- esta rutina recibe time_

    kpis_df = average_kpis(time_)
    if kpis_df.empty:
        return

    # merge de candidates_df con kpis_df

    # rule: a la tabla transactions sólo entran candidatos con
    #       80 < user_avg < 200

    # si cumple las condiciones y NO EXISTE en la tabla transactions
    # debe entrar a la tabla y registrarse allí los valores iniciales
    # de los kpi para hacer las comparaciones posteriores.

    # Idea Evaluator(time_, cellname) # decide si escribe en la tab transactions,

    for idx in candidates_df.index:
        logger.debug(f"cellname {candidates_df['cellname'][idx]}")

    # Idea Executor < -- > NBI : podría ser un proceso independiente
    # - tengo q revisar q retorna el NBI
    # actualiza tablas transactions y rets
