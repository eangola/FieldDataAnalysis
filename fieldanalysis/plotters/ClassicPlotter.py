#!/usr/bin/env python
"""
Created : 06-12-2018
Last Modified : Tue 15 Jan 2019 06:46:35 PM EST
Created By : Enrique D. Angola
"""
from matplotlib import pylab as plt
import seaborn as sns
import numpy as np

class ClassicPlotter():
    """
    Contains methods to generate classic analyses plots

    Parameters
    ----------
    analyses: analyses object from fieldanalysis.analyses module

    Returns
    -------
    Initializes ClassicPlotter object

    """

    def __init__(self,analyses):
        self.analyses = analyses
        

    def plot_scatter(self,x=None,y=None,newFig=True,title=''):
        """
        generates scatter plot
        """
        if newFig:
            plt.figure()
        plt.scatter(x,y,s=1)
        plt.title(title,fontweight='bold')
    

    def plot_histogram(self,x=None,title='',bins=50,channels=None,sNumbers = None,xlabel=''):
        """


        Parameters
        ----------


        Returns
        -------


        Examples
        --------
        >>>

        """
        fig, axs = plt.subplots()
        hist = axs.hist(x,bins=bins)
        mean = np.mean(x)
        stdev = np.std(x)
        median = np.median(x)
        textstr = '\n'.join(('mean =%.2f' % (mean, ),\
                'median = %.2f' % (median, ),\
                'stdev=%.2f' % (stdev, )))
        axs.text(0.9, 0.78,textstr,horizontalalignment='center',\
                verticalalignment='center',transform=axs.transAxes)
        axs.set_title('Histogram of bias at ' + title,fontweight='bold')
        axs.set_ylabel('Frequency',fontweight='bold')
        axs.set_xlabel(xlabel,fontweight='bold')

        if channels and sNumbers:
            print("Channel %d S.N. %s and Channel %d S.N. %s" %(channels[0],sNumbers[0],channels[1],sNumbers[1]))



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
        plt.figure()
        ratios = self.analyses.compute_ws_ratio(x,y)
        monthlyRatios = ratios.resample('M').mean()
        plt.plot(monthlyRatios,'*-',label=label)
        if label:
            plt.legend()
        if channels and sNumbers:
            print("Channel %d S.N. %s and Channel %d S.N. %s" %(channels[0],sNumbers[0],channels[1],sNumbers[1]))


    def plot_linear_regression(self,measure1,measure2,readData=True,title='',xlabel='',ylabel=''):
        """

        Generates linear regression plot with residuals plot

        Parameters
        ----------
        measure1: Str or Series
        measure2: Str or Series
        readData: Boolean
            set to False if passing Series instead of Strings
        title: Str
            Plot title
        xlabel: Str
        ylabel: Str

        Returns
        -------
        Results: Dict
            see analyses.compute_linear_regression

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
        axs[0].set_title('linear regression '+title,fontweight='bold')
        axs[0].set_xlabel(xlabel,fontweight='bold')
        axs[0].set_ylabel(ylabel,fontweight='bold')
        axs[0].scatter(a,b,s=1)
        #create string for results
        textstr = '\n'.join((r'$\mathrm{r^2}=%.2f$' % (r2, ),\
                r'$\mathrm{mse}=%.2f$' % (mse, ),\
                r'$\mathrm{r}=%.2f$' % (r, )))
        axs[0].text(0.9, 0.78,textstr,horizontalalignment='center',\
                verticalalignment='center',transform = axs[0].transAxes)
        #axs[0].set_ylim(min(b)-10,max(b)*1.1)
        axs[1].plot([min(b),max(b)],[0,0])
        axs[1].set_title('Residuals plot '+title,fontweight = 'bold')
        axs[1].set_xlabel(ylabel,fontweight='bold')
        axs[1].set_ylabel('Residuals',fontweight='bold')
        axs[1].scatter(b,res,s=1)
        plt.tight_layout()


        return results


