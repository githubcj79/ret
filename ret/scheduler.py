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

    # de los anteriores seleccionar a los q min < tilt < max
    # (table rets) <-- tilt más reciente

    engine = get_engine()
    session = get_session(engine=engine)

    # ---------------------------------------------------
    # datetimeid más reciente de overshooters
    max_overshooter = session.query(func.max(Overshooter.datetimeid)).first()
    if not max_overshooter:
        logger.info('No overshooters')
        session.commit()
        session.close()
        return

    # datetimeid más reciente de terrains
    max_terrain = session.query(func.max(Terrain.datetimeid)).first()
    if not max_terrain:
        logger.info('No terrains')
        session.commit()
        session.close()
        return

    # datetimeid más reciente de terrains
    max_ret = session.query(func.max(Ret.datetimeid)).first()
    if not max_ret:
        logger.info('No rets')
        session.commit()
        session.close()
        return

    logger.info('--->')

    # set más reciente de overshooters en terreno plano
    q = session.query(Overshooter,Terrain,Ret).filter(and_(
            Overshooter.cellname == Terrain.cellname,
            Terrain.cellname == Ret.cellname,
            Terrain.is_plain,
            Overshooter.datetimeid == max_overshooter,
            Terrain.datetimeid == max_terrain,
            Ret.datetimeid == max_ret,
        ))

    logger.info('<---')

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
