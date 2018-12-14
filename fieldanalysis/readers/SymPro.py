#!/usr/bin/env python
"""
Created : 03-12-2018
Last Modified : Thu 13 Dec 2018 08:43:59 PM EST
Created By : Enrique D. Angola
"""
import pandas as pd
import pdb
import numpy as np

class SymPro():
    """
    Reads data from symphony pro

    Parameters
    ----------


    Returns
    -------


    """

    def __init__(self,filename):

        self.header = None
        self.filename = filename
        self.data = self._read_data()

    def _read_data(self,header=None):

        if not header:
            header = self._find_header()
        data = pd.read_csv(self.filename,skiprows=header, sep = "\t")
        return data

    def _find_header(self):
        """
        Finds the end of the header file

        Parameters
        ----------
        None

        Returns
        -------
        header: int
            line where header starts

        """
        self.header = []
        with open(self.filename) as f:
            headerEnd = 0
            for line in f:
                if line.lower().find('timestamp') != -1:
                    return headerEnd
                else:
                    self.header.append(line.split())
                    headerEnd += 1

    def get_data(self,fieldname,startDate=None,endDate=None):

        if startDate == None:
            startDate = self.data['Timestamp'].iloc[0]
        if endDate == None:
            endDate = self.data['Timestamp'].iloc[-1]

        timeseries = self.data[fieldname][(self.data['Timestamp'] >= startDate) &\
                (self.data['Timestamp'] <= endDate)]

        return self.data[fieldname]

    def get_fieldnames(self):

        return self.data.keys()

    def get_timeseries(self,fieldname,startDate=None,endDate=None):

        if startDate == None:
            startDate = self.data['Timestamp'].iloc[0]
        if endDate == None:
            endDate = self.data['Timestamp'].iloc[-1]

        timeseries = self.data[['Timestamp',fieldname]][(self.data['Timestamp'] >= startDate) &\
                (self.data['Timestamp'] <= endDate)]

        timeseries = pd.Series(np.array(timeseries[fieldname]),index=\
                pd.DatetimeIndex(timeseries['Timestamp']))
        return timeseries

    def apply_filters(self,filters):

        filtersDict = filters.filtersDict
        for Filter in filtersDict.values():
            if not Filter.empty:
                self.data = self.data[Filter]


    def get_fieldname(self,channel=None,metric=None):
        """


        Parameters
        ----------
        channel: Str
            Channel to look for Ex. 'Ch1'
        metric: Str
            metric to look for Ex. 'Avg'

        Returns
        -------
        fieldname: Str
            fieldname in symph. pro
        None is fieldname is not found

        """
        import re
        expression = channel + '.*_' + metric + '_.*'

        fieldnames = self.get_fieldnames()

        for name in fieldnames:
            tmp = re.search(expression,name)
            if tmp != None:
                return tmp.group()

        return None
