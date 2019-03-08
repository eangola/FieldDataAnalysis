#!/usr/bin/env python
"""
Created : 08-02-2019
Last Modified : Thu 07 Mar 2019 08:22:25 PM EST
Created By : Enrique D. Angola
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy import Column, Integer, String, DateTime, create_engine

engine = create_engine('mssql+pyodbc://user/FusionWindResourceData?driver=ODBC+Driver+17+for+SQL+Server', echo=True)
Base = declarative_base(engine)
inspector = inspect(engine)
con = engine.connect()


class Bookmarks(Base):

    __tablename__ = 'EDFCleaning'
    __table_args__ = {'autoload':True}
    #set timestamp as the primary key
    TimeStamp = Column(DateTime,primary_key=True)
    def __init__(self,TimeStamp):

        self.TimeStamp = TimeStamp


def loadSession():
    metadata = Base.metadata

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

if __name__ == "__main__":

    session = loadSession()
    res = session.query(Bookmarks).all()
