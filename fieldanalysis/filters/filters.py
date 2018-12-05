#!/usr/bin/env python
"""
Created : 05-12-2018
Last Modified : Wed 05 Dec 2018 05:12:49 PM EST
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
        self.filtersDict = {}

    def generate_icing_filter(self,temp,vaneSD):

        if not self.filter['icing']:
            icingFilter = self.data[(temp <= 3) & (vaneSD <= 2)]
            self.filtersDict['icing'] = icingFilter
