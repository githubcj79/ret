#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger

from giver_of_times import giver_of_times

def scheduler(time_=None):
    if not time_:
        return

    logger.debug(f"time_ {time_}")

    # se debe ir a buscar a los que hacen overshooting (más recientes)
    # (table overshooters)

    # de los anteriores seleccionar a los q están en terreno plano
    # (table terrains)

    # de los anteriores seleccionar a los q min < tilt < max
    # (table rets) <-- tilt más reciente

    # entregar los candidatos a mid_term_evaluator()

def main():
    for time_ in giver_of_times():
        scheduler(time_)


if __name__ == '__main__':
    main()
