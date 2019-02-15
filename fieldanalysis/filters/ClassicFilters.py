#!/usr/bin/env python
"""
Created : 05-12-2018
Last Modified : Thu 14 Feb 2019 07:21:18 PM EST
Created By : Enrique D. Angola
"""
import pandas as pd
import pdb

class ClassicFilters():
    """
    Object containing classic filters. Filters need to be generated in order to be applied
    to data

    Parameters
    ----------
    reader: reader object from fieldanalysis.reader module

    Returns
    -------
    Initializes ClassicFilter object to be applied to analysis

    """

    def __init__(self,reader):

        self.data = reader.data
        self.reader = reader
        self.filtersDict = {'icing':pd.Series()}
        self.filtersDict['windspeed'] = pd.Series()
        self.filtersDict['bestsector'] = pd.Series()

    def generate_icing_filter(self,temp,vaneSD,tempThreshold = 3,\
            vaneSDThreshold = 2):
        '''
        generate an icing filter given temperature and vane
        SD field.
        '''
        temp = self.reader.get_timeseries(temp)
        vaneSD = self.reader.get_timeseries(vaneSD)
        if self.filtersDict['icing'].empty:
            icingFilter = ((temp >= tempThreshold) &\
                    (vaneSD >= vaneSDThreshold))
            self.filtersDict['icing'] = icingFilter


    def generate_windspeed_filter(self,wsRef=None,wsThreshold = 3,readData=True):
        """
        Generate wind speed filter setting a predefined threshold
        """
        if readData:
            wsRef = self.reader.get_timeseries(wsRef)
        if self.filtersDict['windspeed'].empty:
            windspeedFilter = (wsRef >= wsThreshold)
            self.filtersDict['windspeed'] = windspeedFilter
        #add another filter
        else:
            windspeedFilter = (wsRef >= wsThreshold)
            self.filtersDict['windspeed'] = (self.filtersDict['windspeed'] &\
                    windspeedFilter)


    def generate_best_sector_filter(self,degRef=None,boom=None,bestSector=30):
        """
        Generates best sector filter given best sector angle and boom angles
        """

        degRef = self.reader.get_timeseries(degRef)
        center = (boom[0]+boom[1])/2
        sector = [center - bestSector/2, center + bestSector/2]
        if self.filtersDict['bestsector'].empty:
            bestsectorFilter = ((degRef >= sector[0]) & (degRef <= sector[1]))
            self.filtersDict['bestsector'] = bestsectorFilter


    def clear_all_filters(self):
        """
        Restarts the object, clearing all generated filters

        """
        self.__init__(self.reader)


    def clear_filter(self,filterKey=None):
        """
        Clears a particular filter, sets it to empty

        Parameters
        ----------
        filterKey: Str
            key of filter to reset

        Returns
        -------
        None

        """
        self.filtersDict[filterKey] = pd.Series()

