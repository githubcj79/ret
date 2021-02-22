#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger
import pandas as pd

from giver_of_times import giver_of_times

def transactions(time_=None):
    logger.debug(f"time_ {time_}")

    if not time_:
        return

def main():
    for time_ in giver_of_times():
        transactions(time_)


if __name__ == '__main__':
    main()
