#!/usr/bin/env python
"""
Created : 13-02-2019
Last Modified : Wed 13 Feb 2019 09:09:08 PM EST
Created By : Enrique D. Angola
"""
from fieldanalysis.readers import SymPro
import pandas as pd
import numpy as np

class Spidar(SymPro):
    """
    Reads data from Spidar file

    Parameters
    ----------
    filename: Str
        path to file

    Returns
    -------
    initializes Spidar object

    """

    def __init__(self,filename):
        super().__init__(filename)

    def _read_data(self):
        with open(self.filename,'r') as f:
            data = pd.read_csv(f)

        data = data.set_index('Timestamp')
        return data
