#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kafka import (
        KafkaProducer,
        KafkaConsumer,
    )
from loguru import logger

import datetime
import json
import random
import time

from event import Event
from settings import (
        ENV,
        CLIENT_ID,
        KAFKA_BROKER_URL,
        MML_TOPIC,
        RST_TOPIC,
    )

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda msg: json.dumps(msg).encode('utf-8'), # we serialize our data to json for efficent transfer
)

logger.info(f"MML_TOPIC {MML_TOPIC} RST_TOPIC {RST_TOPIC}")
consumer = KafkaConsumer(
    RST_TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    auto_offset_reset='latest', # where to start reading the messages at
    enable_auto_commit=True,
    #group_id='event-collector-group-2', # consumer group id
    value_deserializer=lambda m: json.loads(m.decode('utf-8')) # we deserialize our data from json
)

def nbi_processor(time_=None,session_=None,trxs_=None):
    '''
    Esta función recibe el query (trxs_) con todas las transacciones
    a ejecutar.
    Construye un mensaje al NBI con todas ellas.
    Espera el mensaje de respuesta y de acuerdo con lo recibido
    actualiza las transacciones en la BD (transactions y rets)
    '''
    logger.debug(f"time_ {time_} ENV {ENV}")

    if not time_ or not session_ or not trxs_:
        return

    # logger.debug(f"hello !!! ..")


    '''
    {
    'object_id': 14144,
    'data': {
       'command': 'MOD CELLDLSCHALGO:LOCALCELLID=0,DLEPFCAPACITYFACTOR=EPF_CAPC_FACTOR_1;',
        'network_element': 'MBTS-VAL_3G_138'
            }
    },
    '''

    # RET Command
    # MOD RETSUBUNIT:DEVICENO=0,SUBUNITNO=1,TILT=60;{MBT-RM2023}

    command_list = []

    for trx in trxs_:
        logger.info(f"trx \n{trx}")
        object_id = 14144
        command = (
                    f'MOD RETSUBUNIT:DEVICENO={trx.deviceno},'
                    f'SUBUNITNO={trx.subunitno},'
                    f'TILT={trx.newtilt};'
                    # '{'
                    # f'{trx.node}'
                    # '}'
                    ),
        network_element = f'{trx.node}',
        dict_ = {
            # 'object_id': object_id, # original
            'object_id': trx.id, # para probar si puedo hilar con la trx
            'data': {
                'command': command,
                'network_element': network_element
            }
        }
        command_list.append(dict_)


    random_script_id = str(random.randint(0, 1e6)).zfill(6)+\
                        ' '+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data = {
        'client_id': CLIENT_ID,
        'script_id': random_script_id,
        'command_type': ['MOD'],
        'timestamp':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'timeout':-1,
        'priority':0,
        'corre_id':20,
        'command_list': command_list
    }

    event_ = Event(type_='mml_type', data=data)
    id_ = event_.id_
    logger.info(f"id_ {id_} ENV {ENV}")

    producer.send(MML_TOPIC, value=event_.as_dictionary())
    logger.info(f"after producer.send(MML_TOPIC ..)")
    logger.info(f"MML_TOPIC {MML_TOPIC}")

    for m in consumer:
        logger.info(f"after for m in consumer:")
        if id_  == m.value['id_']:
            print("*** match", flush=True)
            '''
            - para cada comando ejecutado, estudiar respuesta y
                actualizar trxs y rets, si corresponde
            '''
            break
        else:
            print("continue", flush=True)
            continue
