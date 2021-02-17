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

    # datetimeid más reciente de rets
    max_ret = session.query(func.max(Ret.datetimeid)).first()
    if not max_ret:
        logger.info('No rets')
        session.commit()
        session.close()
        return

    logger.info('--->')
    # set más reciente de overshooters en terreno plano
    # records = session.query(Overshooter,Terrain,Ret).filter(and_(
    #         Overshooter.cellname == Terrain.cellname,
    #         Terrain.cellname == Ret.cellname,
    #         Terrain.is_plain,
    #         Overshooter.datetimeid == max_overshooter,
    #         Terrain.datetimeid == max_terrain,
    #         Ret.datetimeid == max_ret
    #     )).all()

    ''' bad ...
    # Execute a SELECT query on JOINed tables
    records = session.query(Ret).join(Overshooter, Ret.cellname == Overshooter.cellname).all()

    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    # Loop through results
    for record in records:
        record_object = {
            'cellname': record.cellname,
            'overshooters': []
        }
        for overshooter in record.overshooter:
            overshooter = {
                'overshooter_id': overshooter.id,
            }
            record_object['overshooters'].append(overshooter)
            pp.pprint(record_object)
        '''

    ''' esto funciona ...
    # Execute a SELECT query on JOINed tables
    records = session.query(Ret).join(Overshooter, Ret.cellname == Overshooter.cellname).all()

    for record in records:
        print(record)
    '''

    # Execute a SELECT query on JOINed tables
    records = session.query(Ret).join(Overshooter, Ret.cellname == Overshooter.cellname).all()

    for record in records:
        print(record)

    ''' esto funciona ...
    # Fetch all customer records
    records = session.query(Ret).all()

    # Loop over records
    for record in records:
        print(record)
    '''

    # for record in records:
    #     logger.info('?')

    # logger.debug(f'type q.all() {type(q.all())}')
    # for row in q.all():
    #     logger.debug(f'type row {type(row)}')
    #     logger.debug(f'row {row}')
    logger.info('<---')
    # ---------------------------------------------------

    session.commit()
    session.close()

    # entregar los candidatos a mid_term_evaluator()

def main():
    for time_ in giver_of_times():
        scheduler(time_)


if __name__ == '__main__':
    main()
