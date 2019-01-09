#!/usr/bin/env python
"""
Created : 09-01-2019
Last Modified : Wed 09 Jan 2019 10:44:56 AM EST
Created By : Enrique D. Angola
"""

import SymPro


class Campbell(SymPro):
    """
    Reads data from campbell logger programmed by Henry Bush

    Parameters
    ----------


    Returns
    -------


    """

    def __init__(self,filename):

        self.header = None
        self.filename = filename
        self.data = self._read_data()
        self.nonFilteredData = self.data


