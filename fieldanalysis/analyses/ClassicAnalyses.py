#!/usr/bin/env python
"""
Created : 06-12-2018
Last Modified : Fri 14 Dec 2018 03:04:15 PM EST
Created By : Enrique D. Angola
"""


class ClassicAnalyses():
    """


    Parameters
    ----------


    Returns
    -------


    Examples
    --------
    >>>

    """

    def __init__(self,reader=None,startDate = None, endDate = None):
        self.reader = reader
        self.startDate = startDate
        self.endDate = endDate

    def compute_ws_ratio(self,anem1=None,anem2=None):

        """
        Computes wind speed ratio between two anemometers

        Parameters
        ----------
        anem1: Str
            anemometer 1 average fieldname
        anem2: Str
            anemometer 2 average fieldname

        Returns
        -------
        ratio: Pandas Series
            Timeseries of the computed ratio


        """

        anem1 = self.reader.get_timeseries(anem1,self.startDate,self.endDate)
        anem2 = self.reader.get_timeseries(anem2,self.startDate,self.endDate)
        ratio = anem1/anem2
        return ratio


    def compute_TI(self,anemAvg=None,anemSD=None):
        """
        Computes TI for one anemometer

        Parameters
        ----------
        anemAvg = Str
            anemometer average fieldname
        anemSD = Str
            anemometer standard deviation fieldname

        Returns
        -------
        TI = Float
            turbulence intensity

        Examples
        --------

        """
        anemAvg = self.reader.get_data(anemAvg)
        anemSD = self.reader.get_data(anemSD)

        TI = 100*np.mean(anemSD/anemAvg)

        return TI
