#!/usr/bin/env python
"""
Created : 09-01-2019
Last Modified : Fri 11 Jan 2019 02:18:12 PM EST
Created By : Enrique D. Angola
"""
from fieldanalysis.readers import SymPro
import numpy as np
import pdb


class Campbell(SymPro):
    """
    Reads data from campbell logger programmed by Henry Bush this class
    inherits from SymPro

    Parameters
    ----------
    filename: str
        path to file

    Returns
    -------
    Initializes Campbell reader object

    """

    def __init__(self,filename):

        self.header = None
        self.filename = filename
        self.data = self._read_data()
        self.nonFilteredData = self.data
        self.names = None

    def _read_data(self,header=None,sep=","):
        """
        Private method reads data from Campbell file into pandas data frame
        """
        data = super(Campbell, self)._read_data(sep = sep)
        data = data.rename({'TIMESTAMP':'Timestamp'},axis='columns')
        data = data.replace('NAN',np.nan)
        #data = data.dropna()
        data.loc[:,data.columns != 'Timestamp'] = data.loc[:,data.columns != 'Timestamp'].astype(float)
        return data

    def _find_header(self,delimiter='rn'):
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
        headerEnd = super(Campbell, self)._find_header(delimiter)
        headerEnd += 2
        self.names = self.header[1][0].split(',')
        self.names = [element.replace('"','') for element in self.names]
        return headerEnd
