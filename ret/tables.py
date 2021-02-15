#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger

from sqlalchemy import (
        Boolean,
        Column,
        DateTime,
        ForeignKey,
        Index,
        Integer,
        String,
        create_engine,
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
        relationship,
        sessionmaker,
    )

from settings import ENV, ECHO, DB_STR_CONNECTION

BASE = declarative_base()

class Overshooter(BASE):
    __tablename__ = 'overshooters'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    cell_name = Column(String(250), nullable=False)
    time_advanced = Column(Integer, nullable=False)
    average_distance = Column(Integer, nullable=False)
    is_overshooter = Column(Boolean)
    __table_args__ = (
                        Index('my_index1', "date_time", "cell_name"),
                        Index('my_index2', "date_time", "is_overshooter"),
                     )

    def __repr__(self):
        return (f"Overshooter(id[{self.id}],"
                f"date_time[{self.date_time}],"
                f"cell_name[{self.cell_name}],"
                f"time_advanced[{self.time_advanced}],"
                f"average_distance[{self.average_distance}],"
                f"is_overshooter[{self.is_overshooter}])"
                )

class Terrain(BASE):
    __tablename__ = 'terrains'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    cell_name = Column(String(250), nullable=False)
    is_plain = Column(Boolean)
    slope = Column(Integer, nullable=False)
    __table_args__ = (
                        Index('my_index1', "date_time", "cell_name"),
                        Index('my_index2', "date_time", "is_plain"),
                     )

    def __repr__(self):
        return (f"Terrain(id[{self.id}],"
                f"date_time[{self.date_time}],"
                f"cell_name[{self.cell_name}],"
                f"time_advanced[{self.time_advanced}],"
                f"average_distance[{self.average_distance}]",
                f"is_plain[{self.is_plain}])"
                )

class Ret(BASE):
    __tablename__ = 'rets'
    id = Column(Integer, primary_key=True)
    # dateid = Column(DateTime)
    dateid = Column(String(128))
    node = Column(String(128))
    devicename = Column(String(128))
    deviceno = Column(Integer)
    tilt = Column(Integer)
    subname = Column(String(128))
    subunitno = Column(Integer)
    localcellid = Column(Integer)
    eci = Column(Integer)
    __table_args__ = (
                        Index('my_index1', "dateid", "node", "devicename"),
                     )

    def __repr__(self):
        return (f"Ret(id[{self.id}],"
                f"dateid[{self.dateid}],"
                f"node[{self.node}],"
                f"devicename[{self.devicename}],"
                f"deviceno[{self.deviceno}],"
                f"tilt[{self.tilt}],"
                f"subname[{self.subname}],"
                f"subunitno[{self.subunitno}],"
                f"localcellid[{self.localcellid},]"
                f"eci[{self.eci}])"
                )

# ------------------------------------------------
class Transaction(BASE):
    '''
    This is the class that supports the close looped anntenas transactions.
    An anntena is identified by: node, cellname, deviceno.
    created: when the anntena was created in this table.
    generation: when the transaction was created in this table.
    sent: when the command was sent.
    success: if the command ended succesfully.
    failure: if the command ended with a failure.
    '''
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    node = Column(String(128))
    cellname = Column(String(250), nullable=False)
    deviceno = Column(Integer)
    subunitno = Column(Integer)
    tilt = Column(Integer)
    oldtilt = Column(Integer)
    newtilt = Column(Integer)
    created = Column(DateTime)
    generation = Column(DateTime)
    sent = Column(DateTime)
    success = Column(DateTime)
    failure = Column(DateTime)
    __table_args__ = (
                        Index('index1', "cellname", "deviceno"),
                        Index('index2', "node", "cellname", "deviceno"),
                     )

    def __repr__(self):
        return (f"Transaction(id[{self.id}],"
                f"node[{self.node}],"
                f"cellname[{self.cellname}],"
                f"deviceno[{self.deviceno}],"
                f"subunitno[{self.subunitno}],"
                f"tilt[{self.tilt}],",
                f"oldtilt[{self.oldtilt}],"
                f"newtilt[{self.newtilt}],"
                f"created[{self.generation}],"
                f"generation[{self.generation}],"
                f"sent[{self.sent}],"
                f"success[{self.success}],"
                f"failure[{self.failure}])"
                )
# ------------------------------------------------

def get_engine():
    logger.info(f'get_engine:')
    return create_engine(DB_STR_CONNECTION, echo=ECHO)

def get_session(engine=None):
    if not engine:
        return None
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables():
    logger.info(f'create_tables:')
    engine = get_engine()
    BASE.metadata.create_all(engine)
    return True

create_tables()

def main():
    create_tables()


if __name__ == '__main__':
    main()
