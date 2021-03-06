# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column, Integer, Float, DateTime, BigInteger
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from telegram import Bot

from config import DB

ENGINE = create_engine(DB,
                       echo=False,
                       pool_size=200,
                       max_overflow=50,
                       isolation_level="READ UNCOMMITTED")

LOGGER = logging.getLogger('sqlalchemy.engine')
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=ENGINE))


class Device(Base):
    __tablename__ = 'device_data'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    device_id = Column(BigInteger)
    date = Column(DateTime, default=datetime.now())
    temp = Column(Float)
    hum = Column(Float)
    ppm = Column(Integer)


def user_allowed(func):
    def wrapper(bot: Bot, update, *args, **kwargs):
        session = Session()
        try:
            func(bot, update, session, *args, **kwargs)
        except SQLAlchemyError as err:
            bot.logger.error(str(err))
            session.rollback()
    return wrapper


Base.metadata.create_all(ENGINE)
