#!/usr/bin/env python
"""
Created : 06-12-2018
Last Modified : Tue 08 Jan 2019 02:36:11 PM EST
Created By : Enrique D. Angola
"""
from matplotlib import pylab as plt
import seaborn as sns
import numpy as np

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

    def plot_scatter(self,x=None,y=None,newFig=True):
        if newFig:
            plt.figure()
        plt.scatter(x,y,s=1)


    def plot_monthly_ratios(self,x,y,label=None,channels=None,sNumbers = None):
        """
        Computes ratios by month and plots them

        Parameters
        ----------
        x: Str
            Fieldname for anem 1
        y: Str
            Fieldname for anem 2
        label: Str
            Label for plot

        Returns
        -------
        None

        """
        ratios = self.analyses.compute_ws_ratio(x,y)
        monthlyRatios = ratios.resample('M').mean()
        plt.plot(monthlyRatios,'*-',label=label)
        if label:
            plt.legend()
        if channels and sNumbers:
            print("Channel %d S.N. %s and Channel %d S.N. %s" %(channels[0],sNumbers[0],channels[1],sNumbers[1]))


    def plot_linear_regression(self,measure1,measure2,readData=True):
        """


        Parameters
        ----------


        Returns
        -------


        Examples
        --------
        >>>

        """
        results = self.analyses.compute_linear_regression(measure1,\
                measure2,readData)

        a = results['measure1']
        b = results['measure2']
        r = results['r']
        r2 = results['r2']
        mse = results['mse']
        params = results['params']
        res = results['residuals']
        #define y for plot
        y = np.linspace(min(a),max(a),1000)*params[0] + params[1]
        fig, axs = plt.subplots(nrows=2, ncols=1)
        axs[0].plot(np.linspace(min(a),max(a),1000),y)
        axs[0].set_title('linear regression')
        axs[0].scatter(a,b)
        #create string for results
        textstr = '\n'.join((r'$\mathrm{r^2}=%.2f$' % (r2, ),\
                r'$\mathrm{mse}=%.2f$' % (mse, ),\
                r'$\mathrm{r}=%.2f$' % (r, )))
        axs[0].text(0.9, 0.78,textstr,horizontalalignment='center',\
                verticalalignment='center',transform = axs[0].transAxes)
        #axs[0].set_ylim(min(b)-10,max(b)*1.1)
        axs[1].plot([min(b),max(b)],[0,0])
        axs[1].set_title('residuals')
        axs[1].plot(b,res,'.')
        plt.tight_layout()


        return results


