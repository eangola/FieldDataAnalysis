#!/usr/bin/env python
"""
Created : 11-02-2019
Last Modified : Mon 11 Feb 2019 07:36:46 PM EST
Created By : Enrique D. Angola
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy import Column, Integer, String, DateTime, create_engine
import pandas as pd
import pdb
import numpy as np

class DataBase(Base):

    __tablename__ = 'EDFCleaning' #PLACE HOLDER
    __table_args__ = {'autoload':True}
    #set timestamp as the primary key
    TimeStamp = Column(DateTime,primary_key=True)
    def __init__(self,TimeStamp):
        self.TimeStamp = TimeStamp


#if __name__ == "__main__":
 #   session = loadSession()
 #  res = session.query(Bookmarks).all()


class Fusion():
    """
    Connects to Fusion database and allows SQL queries

    """

    def __init__(self):
        self.setup = self._setup()
        self.session = self._load_session()

    def _setup():

        engine = create_engine('mssql+pyodbc://dsuser:dbuser1231$#ASDF!@nrgfusion.database.windows.net:1433/FusionWindResourceData?driver=ODBC+Driver+17+for+SQL+Server', echo=True)
        Base = declarative_base(engine)
        inspector = inspect(engine)
        con = engine.connect()
        setup = {'con':con,'engine':engine,'Base':Base,'inspector':inspector}
        return setup

    def _load_session():
        metadata = Base.metadata

        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def _read_data(self,startDate=None,endDate=None,column = None):

        if startDate and column:
            rs = session.query(DataBase).filer('TimeStamp' ....).column
        elif startDate:
            rs = session.query(DataBase).filer('TimeStamp' ....).all
        elif column:
            rs = session.query(DataBase).column
        else:
            rs = session.query(DataBase).all
