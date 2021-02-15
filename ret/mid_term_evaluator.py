#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger

from giver_of_times import giver_of_times

def mid_term_evaluator(time_=None):
    if not time_:
        return

    logger.debug(f"time_ {time_}")

def main():
    for time_ in giver_of_times():
        mid_term_evaluator(time_)


if __name__ == '__main__':
    main()
