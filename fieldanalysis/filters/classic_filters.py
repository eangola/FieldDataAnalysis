#!/usr/bin/env python
"""
Created : 05-12-2018
Last Modified : Fri 21 Dec 2018 05:15:46 PM EST
Created By : Enrique D. Angola
"""
import pandas as pd

class filters():
    """


    Parameters
    ----------


    Returns
    -------


    Examples
    --------
    >>>

    """

    def __init__(self,reader):

        self.data = reader.data
        self.reader = reader
        self.filtersDict = {'icing':pd.Series()}
        self.filtersDict['windspeed'] = pd.Series()

    def generate_icing_filter(self,temp,vaneSD,tempThreshold = 3,\
            vaneSDThreshold = 2):
        '''
        generate an icing filter given temperature and vane
        SD field.
        '''
        temp = self.reader.get_data(temp)
        vaneSD = self.reader.get_data(vaneSD)
        if self.filtersDict['icing'].empty:
            icingFilter = ((temp >= tempThreshold) &\
                    (vaneSD >= vaneSDThreshold))
            self.filtersDict['icing'] = icingFilter


    def generate_windspeed_filter(wsRef=None,wsThreshold = 3):
        """


        Parameters
        ----------


        Returns
        -------


        Examples
        --------
        >>>

        """
        wsRef = self.reader.get_data(wsRef)
        if self.filtersDict['windspeed'].empty:
            windspeedFilter = (wsRef >= wsThreshold)
            self.filtersDict['windspeed'] = windspeedFilter

    
    def generate_best_sector_filter(self,degRef=None,boom=None,bestSector=30):
        """


        Parameters
        ----------


        Returns
        -------


        Examples
        --------
        >>>

        """

        degRef = self.reader.get_data(degRef)
        center = (boom[0]+boom[1])/2
        sector = [center - bestSector/2, center + bestSector/2]
        if self.filtersDict['bestsector'].empty:
            bestsectorFilter = (degRef >= sector[0]) and (degRef <= sector[1])
            self.bestsectorFilter['bestsector'] = bestsectorFilter
