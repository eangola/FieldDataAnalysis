#!/usr/bin/env python
"""
Created : 03-12-2018
Last Modified : Tue 04 Dec 2018 08:35:42 PM EST
Created By : Enrique D. Angola
"""
import pandas as pd
import pdb


class SymPro():
    """


    Parameters
    ----------


    Returns
    -------


    Examples
    --------
    >>>

    """

    def __init__(self,filename):
        self.filename = filename
        self.data = None
        self.header = None

    def read_data(self,header=None):

        if not header:
            header = self._find_header()
        self.data = pd.read_csv(self.filename,skiprows=header, sep = "\t")


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

    def get_data(self,fieldname):

        return self.data[fieldname]

    def get_fieldnames(self):

        return self.data.keys()

    def get_timeseries(self,fieldname,startDate=None,endDate=None):

        if startDate == None:
            startDate = self.data['Timestamp'].iloc[0]
        if endDate == None:
            endDate = self.data['Timestamp'].iloc[-1]

        timeseries = self.data[['Timestamp',fieldname]][(self.data['Timestamp'] >= startDate) &\
                (self.data['Timestamp'] <= endDate)
