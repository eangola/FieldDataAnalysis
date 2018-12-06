#!/usr/bin/env python
"""
Created : 05-12-2018
Last Modified : Thu 06 Dec 2018 05:39:25 PM EST
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
        self.filtersDict['windspeed':None}

    def generate_icing_filter(self,temp,vaneSD,tempThreshold = 3,\
            vaneSDThreshold = 2):
        '''
        generate an icing filter given temperature and vane
        SD field.
        '''
        temp = self.reader.get_data(temp)
        vaneSD = self.reader.get_data(vaneSD)
        if not self.filtersDict['icing']:
            icingFilter = ((temp >= tempThreshold) &\
                    (vaneSD >= vaneThreshold))
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
        if not self.filtersDict['windspeed']:
            windspeedFilter = (wsRef >= wsThreshold)
            self.filtersDict['windspeed'] = windspeedFilter

