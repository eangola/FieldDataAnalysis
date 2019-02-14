#!/usr/bin/env python
"""
Created : 06-12-2018
Last Modified : Thu 14 Feb 2019 05:01:27 PM EST
Created By : Enrique D. Angola
"""
from matplotlib import pylab as plt
import seaborn as sns
import numpy as np
from scipy import stats

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

    def __init__(self,analyses,startDate=None,endDate=None):
        self.analyses = analyses
        self.startDate = startDate
        self.endDate = endDate

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
        kurtosis = stats.kurtosis(x)
        skew = stats.skew(x)
        textstr = '\n'.join(('mean =%.2f' % (mean, ),\
                'median = %.2f' % (median, ),\
                'stdev=%.2f' % (stdev, )))

        textstr2 = '\n'.join(('kurtosis =%.2f' % (kurtosis, ),\
                'skewness = %.2f' % (skew, )))

        axs.text(0.9, 0.78,textstr,horizontalalignment='center',\
                verticalalignment='center',transform=axs.transAxes)
        axs.text(0.2, 0.78,textstr2,horizontalalignment='center',\
                verticalalignment='center',transform=axs.transAxes)

        axs.set_title('Histogram ' + title,fontweight='bold')
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


    def plot_linear_regression(self,measure1,measure2,readData=True,estimate=None,title='',xlabel='',ylabel=''):
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
                measure2,readData,estimate=estimate)

        a = results['measure1']
        b = results['measure2']
        r = results['r']
        r2 = results['r2']
        mse = results['mse']
        params = results['params']
        res = results['residuals']
        predicted = results['predicted']
        #define y for plot
        y = np.linspace(min(a),max(a),1000)*params[0] + params[1]
        fig, axs = plt.subplots(nrows=2, ncols=1)
        axs[0].plot(np.linspace(min(a),max(a),1000),y,color='red')
        axs[0].set_title('linear regression '+title,fontweight='bold')
        axs[0].set_xlabel(xlabel,fontweight='bold')
        axs[0].set_ylabel(ylabel,fontweight='bold')
        axs[0].scatter(a,b,s=1)
        #create string for results
        textstr = '\n'.join((r'$\mathrm{r^2}=%.2f$' % (r2, ),\
                r'$\mathrm{mse}=%.4f$' % (mse, ),\
                r'$\mathrm{r}=%.2f$' % (r, )))
        axs[0].text(0.9, 0.78,textstr,horizontalalignment='center',\
                verticalalignment='center',transform = axs[0].transAxes)
        #axs[0].set_ylim(min(b)-10,max(b)*1.1)
        axs[1].plot([min(predicted),max(predicted)],[0,0],color='red')
        axs[1].set_title('Residuals plot '+title,fontweight = 'bold')
        axs[1].set_xlabel('predicted '+ylabel,fontweight='bold')
        axs[1].set_ylabel('Residuals',fontweight='bold')
        axs[1].scatter(predicted,res,s=1)
        plt.tight_layout()


        return results


    def plot_windrose(self,windSpeed,windDirection,readData=True):
        """
        Plot Windrose
        """
        from windrose import WindroseAxes
        import matplotlib.cm as cm

        if readData:
            windSpeed = self.analyses.reader.get_timeseries(windSpeed,self.startDate,self.endDate)
            windDirection = self.analyses.reader.get_timeseries(windDirection,self.startDate,self.endDate)

        ax = WindroseAxes.from_ax()
        ax.bar(windDirection,windSpeed,normed=True,opening = 0.8, edgecolor='white')
        ax.set_legend()


    def plot_spectra(self,measure,fs,readData=True,**kwargs):
        """


        Parameters
        ----------


        Returns
        -------


        Examples
        --------
        >>>

        """
        freq,den = self.analyses.compute_welch_spectra(measure,fs,readData,**kwargs)
        ax = plt.subplot(1,1,1)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.plot(freq,den)
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel('U*S(t)(L^3/T^2)')
        ax.grid(True,which="both",ls="-")

