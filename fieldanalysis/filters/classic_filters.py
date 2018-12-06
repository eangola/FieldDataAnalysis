#!/usr/bin/env python
"""
Created : 05-12-2018
Last Modified : Wed 05 Dec 2018 08:17:50 PM EST
Created By : Enrique D. Angola
"""

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
        self.filtersDict = {'icing':None}

    def generate_icing_filter(self,temp,vaneSD):
        temp = self.reader.get_data(temp)
        vaneSD = self.reader.get_data(vaneSD)
        if not self.filtersDict['icing']:
            icingFilter = ((temp >= 3) & (vaneSD >= 2))
            self.filtersDict['icing'] = icingFilter
