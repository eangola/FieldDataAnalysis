#!/usr/bin/env python
"""
Created : 11-02-2019
Last Modified : Mon 11 Feb 2019 08:08:37 PM EST
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


#if __name__ == "__main__":
 #   session = loadSession()
 #  res = session.query(Bookmarks).all()


class Fusion():
    """
    Connects to Fusion database and allows SQL queries

    """

    def __init__(self):
        from fieldanalysis.readers import _connectFusion as CF
        self.session = CF.loadSession()

    def _read_data(self,startDate=None,endDate=None,column = None):

#        if startDate and column:
#            rs = session.query(DataBase).filer('TimeStamp' ....).column
#        elif startDate:
#            rs = session.query(DataBase).filer('TimeStamp' ....).all
#        elif column:
#            rs = session.query(DataBase).column
#        else:
#            rs = session.query(DataBase).all
        pass
