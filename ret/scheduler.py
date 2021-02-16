#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import (
        func,
        and_,
    )
from loguru import logger

from giver_of_times import giver_of_times

from tables import (
        Overshooter,
        Terrain,
        Ret,
        get_engine,
        get_session,
    )

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

    engine = get_engine()
    session = get_session(engine=engine)

    # ---------------------------------------------------
    max_overshooter = session.query(func.max(Overshooter.datetimeid)).first()
    if not max_overshooter:
        logger.info('No overshooters')
        session.commit()
        session.close()
        return

    logger.info('--->')


   #  datetimeid_latest_overshooter

   #          row = self.session.query(func.max(Tweet.status_id)).first()
   #      if row is not None:
   #          since_id = row[0] if row[0] is not None else 0
   #      else:
   #          since_id = 0


   #  q = session.query(Overshooter,Terrain,Ret).filter(
   #          Overshooter.)







   #  exists = session.query(Transaction).filter(and_(
   #                          Transaction.node==antenna.node,
   #                          Transaction.cellname==antenna.cellname,
   #                          Transaction.deviceno==antenna.deviceno,
   #                              )
   #                          ).first()

   # from sqlalchemy_sample import session, User, Car

   #  #On a single column
   #  q = session.query(User, Car).filter(User.username==Car.owner_name)
   #  for row in q:
   #      print row
    # ---------------------------------------------------

    session.commit()
    session.close()

    # entregar los candidatos a mid_term_evaluator()

def main():
    for time_ in giver_of_times():
        scheduler(time_)


if __name__ == '__main__':
    main()
