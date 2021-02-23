#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger

def processor(time_=None,session_=None,trx_=None):
    logger.debug(f"time_ {time_}")

    if not time_ or not session_ or not trx_:
        pass

    logger.info(f"trx_ \n{trx_}")
