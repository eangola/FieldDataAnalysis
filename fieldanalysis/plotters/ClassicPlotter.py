#!/usr/bin/env python
"""
Created : 06-12-2018
Last Modified : Tue 11 Dec 2018 02:49:26 PM EST
Created By : Enrique D. Angola
"""
from matplotlib import pylab as plt
import seaborn as sns

class ClassicPlotter():
    """


    Parameters
    ----------


    Returns
    -------


    Examples
    --------
    >>>

    """

    def __init__(self,analyses):
        self.analyses = analyses

    def plot_scatter(self,x=None,y=None):
        plt.scatter(x,y)
