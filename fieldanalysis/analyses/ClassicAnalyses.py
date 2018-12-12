#!/usr/bin/env python
"""
Created : 06-12-2018
Last Modified : Tue 11 Dec 2018 07:21:06 PM EST
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

    def ws_ratio(self,anem1=None,anem2=None):
        anem1 = self.reader.get_timeseries(anem1,self.startDate,self.endDate)
        anem2 = self.reader.get_timeseries(anem2,self.startDate,self.endDate)
        ratio = anem1/anem2
        return ratio

