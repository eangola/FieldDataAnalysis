#!/usr/bin/env python
"""
Created : 03-12-2018
Last Modified : Fri 11 Jan 2019 02:23:20 PM EST
Created By : Enrique D. Angola
"""
import pandas as pd
import pdb
import numpy as np

class SymPro():
    """
    Reads data from symphony pro logger file

    Parameters
    ----------
    filename: Str
        path to file

    Returns
    -------
    Initializes SymPro object

    """

    def __init__(self,filename):

        self.names=None
        self.header = None
        self.filename = filename
        self.data = self._read_data()
        self.nonFilteredData = self.data

    def _read_data(self,header=None,sep="\t"):
        """
        private method reads data from sympro logger format into a data frame
        """
        if not header:
            header = self._find_header()
        data = pd.read_csv(self.filename,skiprows=header, sep = sep,names=self.names)
        return data

    def _find_header(self,delimiter='timestamp'):
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
                if line.lower().find(delimiter) != -1:
                    return headerEnd
                else:
                    self.header.append(line.split())
                    headerEnd += 1

    def get_data(self,fieldname,startDate=None,endDate=None):

        """
        Retrieve dataframe

        Parameters
        ----------
        fieldname: Str
            Fieldname of column to retrieve
        startDate: Str
            start date, if None, returs all values
        endDate: Str
            end date, if None, returns all values

        Returns
        -------
        Dataframe
            Pandas dataframe of requested data column

        """

        if startDate == None:
            startDate = self.data['Timestamp'].iloc[0]
        if endDate == None:
            endDate = self.data['Timestamp'].iloc[-1]

        timeseries = self.data[fieldname][(self.data['Timestamp'] >= startDate) &\
                (self.data['Timestamp'] <= endDate)]

        return self.data[fieldname]

    def get_fieldnames(self):
        """
        Returns all keys (fieldnames) for data columns
        """

        return self.data.keys()

    def get_timeseries(self,fieldname,startDate=None,endDate=None):
        """
        Retrieve pandas time-series of specified data column

        Parameters
        ----------
        fieldname: Str
            Fieldname of column to retrieve
        startDate: Str
            start date, if None, returs all values
        endDate: Str
            end date, if None, returns all values

        Returns
        -------
        Timeseries: Pandas time-series
            Pandas time-series of requested data column

        """

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

        """
        Applies filter object to data

        Parameters
        ----------
        filters: Filter object

        Returns
        -------
        None

        """

        filtersDict = filters.filtersDict
        #start with all True (no filter)
        finalFilter = pd.Series([True for i in range(len(self.data))])
        #set index of finalFilter = self.data.index so that filter and data index match
        finalFilter.index = self.data.index
        #merge filters
        for Filter in filtersDict.values():
            #if a filter is empty, it will set all to False
            if not Filter.empty:
                finalFilter = (finalFilter & Filter)

        #apply merged filters
        self.data = self.data[finalFilter]

    def remove_filters(self):
        """
        Remove all filters from data

        """
        self.data = self.nonFilteredData

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
        None: if fieldname is not found

        """
        import re
        expression = channel + '.*_' + metric + '_.*'

        fieldnames = self.get_fieldnames()

        for name in fieldnames:
            tmp = re.search(expression,name)
            if tmp != None:
                return tmp.group()

        return None


    def get_info(self,channel):
        """
        Retrieves info of sensor in tower

        Parameters
        ----------
        channel: Int
            Sensor channel

        Returns
        -------
        info: Dict
            keys: sType,height,brand,sNumber,scale,offset
            values: Strings

        """
        for i,value in enumerate(self.header):
            if value == ['Channel:', str(channel)]:
                sType = self.header[i+2][1]
                height = self.header[i+5][1]
                brand = self.header[i+3][1:]
                sNumber = self.header[i+4][-1]
                scale = self.header[i+7][-1]
                offset = self.header[i+8][-1]


        info = {'sType':sType,'height':height,'brand':brand,'sNumber':sNumber,'scale':scale,'offset':offset}

        return info

