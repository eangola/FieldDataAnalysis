#!/usr/bin/env python
"""
Created : 13-02-2019
Last Modified : Wed 13 Feb 2019 08:48:04 PM EST
Created By : Enrique D. Angola
"""
import pandas as pd
import pdb
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

    def __init__(self,arg):


    def _read_data(self,arg):
        with open(self.filename,'r') as f:
            data = pd.read_csv(f)

        data = data.set_index('Timestamp')
        return data
        return x
