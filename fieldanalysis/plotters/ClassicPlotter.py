#!/usr/bin/env python
"""
Created : 06-12-2018
Last Modified : Thu 06 Dec 2018 08:00:04 PM EST
Created By : Enrique D. Angola
"""


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
