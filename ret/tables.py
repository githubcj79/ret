#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loguru import logger

from sqlalchemy import (
        Boolean,
        Column,
        DateTime,
        Float,
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

from settings import (
        ENV,
        ECHO,
        DB_STR_CONNECTION
    )

BASE = declarative_base()

class Overshooter(BASE):
    __tablename__ = 'overshooters'
    id = Column(Integer, primary_key=True)
    datetimeid = Column(DateTime)
    cellname = Column(String(250), nullable=False)
    ta_calculated = Column(Float, nullable=False)
    average_distance = Column(Float, nullable=False)
    overshooter = Column(Boolean)
    intensity = Column(String(250), nullable=False)
    __table_args__ = (
                Index('my_index1', "datetimeid", "cellname"),
                Index('my_index2', "datetimeid", "overshooter"),
                Index('my_index3', "datetimeid", "overshooter", "intensity"),
                )

    def __repr__(self):
        return (f"Overshooter(id[{self.id}],"
                f"datetimeid[{self.datetimeid}],"
                f"cellname[{self.cellname}],"
                f"ta_calculated[{self.ta_calculated}],"
                f"average_distance[{self.average_distance}],"
                f"overshooter[{self.overshooter}],"
                f"intensity[{self.intensity}])"
                )

class Terrain(BASE):
    __tablename__ = 'terrains'
    id = Column(Integer, primary_key=True)
    datetimeid = Column(DateTime)
    cellname = Column(String(250), nullable=False)
    is_plain = Column(Boolean)
    slope = Column(Integer, nullable=False)
    __table_args__ = (
                Index('my_index1', "datetimeid", "cellname"),
                Index('my_index2', "datetimeid", "is_plain"),
                Index('my_index3', "datetimeid", "is_plain", "slope"),
                )

    def __repr__(self):
        return (f"Terrain(id[{self.id}],"
                f"datetimeid[{self.datetimeid}],"
                f"cellname[{self.cellname}],"
                f"is_plain[{self.is_plain}],"
                f"slope[{self.slope}])"
                )

class Ret(BASE):
    __tablename__ = 'rets'
    id = Column(Integer, primary_key=True)
    datetimeid = Column(DateTime)
    node = Column(String(128))
    cellname = Column(String(250), nullable=False)
    eci = Column(Integer)
    devicename = Column(String(128))
    deviceno = Column(Integer)
    tilt = Column(Integer)
    subname = Column(String(128))
    subunitno = Column(Integer)
    localcellid = Column(Integer)
    __table_args__ = (
                        Index('my_index1', "datetimeid", "node", "cellname"),
                     )

    def __repr__(self):
        return (f"Ret(id[{self.id}],"
                f"datetimeid[{self.datetimeid}],"
                f"node[{self.node}],"
                f"cellname[{self.cellname}],"
                f"eci[{self.eci}],"
                f"devicename[{self.devicename}],"
                f"deviceno[{self.deviceno}],"
                f"tilt[{self.tilt}],"
                f"subname[{self.subname}],"
                f"subunitno[{self.subunitno}],"
                f"localcellid[{self.localcellid}])"
                )

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
    user_thrp_dl = Column(Float, nullable=False) # initial value
    traffic_dl = Column(Float, nullable=False) # initial value
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

def get_engine():
    logger.debug(f'get_engine:')
    return create_engine(DB_STR_CONNECTION, echo=ECHO)

def get_session(engine=None):
    if not engine:
        return None
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables():
    logger.debug(f'create_tables:')
    engine = get_engine()
    BASE.metadata.create_all(engine)
    return True

create_tables()

def main():
    create_tables()


if __name__ == '__main__':
    main()
