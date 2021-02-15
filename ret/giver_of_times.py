#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger

import datetime
import time

def giver_of_times():
    '''
    Esta funcion es un generador de tiempos.
    Estos tiempos se asocian a los ciclos.
    Es el reloj del simulador.
    '''
    time_list = [
                    datetime.datetime(2021, 1, 10, 10, 30, 0, 0),
                    datetime.datetime(2021, 1, 11, 10, 30, 0, 0),
                    datetime.datetime(2021, 1, 12, 10, 30, 0, 0),
                    datetime.datetime(2021, 1, 13, 10, 30, 0, 0),
                ]

    seconds = 1

    for time_ in time_list:
        time.sleep(seconds)
        yield time_

def main():
    for time_ in giver_of_times():
        logger.debug(f"time_ {time_}")


if __name__ == '__main__':
    main()
