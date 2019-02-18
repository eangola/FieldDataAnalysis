#!/usr/bin/env python
"""
Created : 06-12-2018
Last Modified : Mon 18 Feb 2019 01:56:33 PM EST
Created By : Enrique D. Angola

Implements classic field data analyses methods for vanes and anemometers.

"""
import pandas as pd
import numpy as np
import pdb

class ClassicAnalyses():

    """
    Methods can be applied to mast data

    Parameters
    ----------
    reader: fieldanalysis.reader object
        data source reader
    startDate: Str
        date to start analysis
    endDate: Str
        date to end analysis

    """

    def __init__(self,reader=None,startDate = None, endDate = None):
        self.reader = reader
        self.startDate = startDate
        self.endDate = endDate

    def compute_ws_ratio(self,anem1=None,anem2=None,readData=True):

        """
        Computes wind speed ratio between two anemometers

        Parameters
        ----------
        anem1: Str
            anemometer 1 average fieldname
        anem2: Str
            anemometer 2 average fieldname

        Returns
        -------
        ratio: Pandas Series
            Timeseries of the computed ratio


        """
        if readData:
            anem1 = self.reader.get_timeseries(anem1,self.startDate,self.endDate)
            anem2 = self.reader.get_timeseries(anem2,self.startDate,self.endDate)

        ratio = anem1/anem2
        return ratio


    def compute_bias(self,sensor1=None,sensor2=None,readData=True):
        """
        Compute bias of two sensors

        Parameters
        ----------
        sensor1 = Str or Pandas Series
            sensor1 average fieldname or series
        sensor2 = Str or Pandas Series
            sensor2 fieldname or series
        readData = bool
            set true if passing fieldnames, False if passing data series

        Returns
        -------

        """
        if readData:
            sensor1 = self.reader.get_timeseries(sensor1,self.startDate,self.endDate)
            sensor2 = self.reader.get_timeseries(sensor2,self.startDate,self.endDate)

        bias = sensor1 - sensor2

        return bias



    def compute_TI(self,anemAvg=None,anemSD=None,readData=True):
        """
        Computes TI for one anemometer

        Parameters
        ----------
        anemAvg = Str
            anemometer average fieldname
        anemSD = Str
            anemometer standard deviation fieldname

        Returns
        -------
        TI = Float
            turbulence intensity

        Examples
        --------

        """
        if readData:
            anemAvg = self.reader.get_timeseries(anemAvg,self.startDate,self.endDate)
            anemSD = self.reader.get_timeseries(anemSD,self.startDate,self.endDate)

        TI = 100*anemSD/anemAvg

        return TI


    def compute_binned_TI(self,anemAvg,anemSD,bins,binBy,meanTI = False):
        """
        Computes binned TI

        Parameters
        ----------
        sensorAvg: Str
            fieldname for sensor average
        sensorSD: Str
            fieldname for sensor SD
        bins: List
            List containing bins
        binBy: Str
            fieldname of metric to bin by

        Returns
        -------
        binnedTI: list
            list containing the binned TI

        """
        #obtain grouped data
        groupAvg = self._bin_data(anemAvg,bins,binBy)
        groupSD = self._bin_data(anemSD,bins,binBy)
        #iterate through data and compute TI
        binnedTI = []
        for key in groupAvg.groups:
            dataAvg = groupAvg.get_group(key)
            dataSD = groupSD.get_group(key)
            if meanTI:
                binnedTI.append(np.mean(self.compute_TI(dataAvg,dataSD,False)))
            else:
                binnedTI.append(self.compute_TI(dataAvg,dataSD,False))


        return binnedTI

    def compute_binned_bias(self,sensor1,sensor2,bins,binBy,meanBias = False):
        """
        Computes binned TI

        Parameters
        ----------
        sensor1: Str
            fieldname for sensor 1
        sensor2: Str
            fieldname for sensor 2
        bins: List
            List containing bins
        binBy: Str
            fieldname of metric to bin by

        Returns
        -------
        binnedBias: list
            list containing the binned bias

        """
        #obtain grouped data
        group1 = self._bin_data(sensor1,bins,binBy)
        group2 = self._bin_data(sensor2,bins,binBy)
        #iterate through data and compute TI
        binnedBias = []
        for key in group1.groups:
            data1 = group1.get_group(key)
            data2 = group2.get_group(key)
            if meanBias:
                binnedBias.append(np.mean(self.compute_bias(data1,data2,False)))
            else:
                binnedBias.append(self.compute_bias(data1,data2,False))


        return binnedBias


    def _bin_data(self,sensor,bins,binBy):
        """
        Bin data by specified bins and criteria

        Parameters
        ----------
        sensor: Str
            Fieldname of measure to bin
        bins: List
            List of bins
        binBy: Str
            Fieldname of measure to use for binning criteria

        Returns
        -------
        group: pandas.core.groupby.SeriesGroupBy
            binned data

        """
        ref = self.reader.get_timeseries(binBy,self.startDate,self.endDate)
        binnedRef = pd.cut(ref,bins)
        data = self.reader.get_timeseries(sensor,self.startDate,self.endDate)
        group = data.groupby(binnedRef)

        return group


    def compute_linear_regression(self,measure1,measure2,readData=True,estimate=None):
        """
        Fits a linear model to 2-D data

        Parameters
        ----------
        measure1: Str or Array of floats
            fieldname of measure 1 or array of values
        measure2: Str or Array of floats
            fieldname of measure 2 or array of values
        readData: Boolean
            if passing data instead of fieldnames, set this to False.

        Returns
        -------
        Dictionary
            keys:
                - parameters: tuple linear model coefficient and intercept
                - r2: r squared (coeff of determination)
                - mse: mean square error
                - r: coefficient of correlation
                - residuals: residuals from (predicted - traininig data)
                - measure1: values of measure 1
                - measure2: values of measure 2
                - predicted: predicted values for measure 2
                - estimate: predicted value for single test value

        """
        from sklearn import datasets, linear_model
        from sklearn.metrics import mean_squared_error, r2_score

        if readData:
            measure1 = self.reader.get_timeseries(measure1,self.startDate,self.endDate)
            measure2 = self.reader.get_timeseries(measure2,self.startDate,self.endDate)

        r = np.corrcoef(measure1,measure2)[0,1] #correlation coefficient

        measure1 = measure1.values.reshape(len(measure1),1)
        measure2 = measure2.values.reshape(len(measure2),1)

        regr = linear_model.LinearRegression()

        regr.fit(measure1,measure2)
        params = (regr.coef_[0],regr.intercept_)

        predict = regr.predict(measure1)
        if estimate:
            prediction = regr.predict(np.asarray(estimate).reshape(-1,1))
        else:
            prediction = None

        r2 = r2_score(measure2,predict) #coefficient of determination, explained variance
        mse = mean_squared_error(measure2,predict,multioutput='raw_values')

        residuals = measure2 - predict

        return {'params':params,'r2':r2,'mse':mse, 'r':r,'residuals':residuals,\
                'measure1':measure1,'measure2':measure2,'predicted':predict,'estimate':prediction}



    def compute_horizontal_wind_magnitude(self,U,V,readData=True):
        """
        Compute the horizontal wind magnitude (X-Y plane) from an ultrasonic sensor

        Parameters
        ----------
        U: Str or array of floats
            Wind speed in X direction
        V: Str or array of floats
            Wind speed in Y direction

        readData: Boolean
            if passing data instead of fieldnames, set this to False.

        Returns
        -------
        horMagnitude: Pandas Series
            Time series of wind speed magnitude

        """
        if readData:
            U = self.reader.get_timeseries(U,self.startDate,self.endDate)
            V = self.reader.get_timeseries(V,self.startDate,self.endDate)
        horMagnitude = np.sqrt(U**2 + V**2)

        return horMagnitude

    def compute_off_axis_angle(self,U=None,V=None,W=None,horMagnitude=None,readData=True):
        """
        Computes angle of the horMagnitude relative to the X-Y plane

        Parameters
        ----------
         U: Str or array of floats
            Wind speed in X direction (optional)
         V: Str or array of floats
            Wind speed in Y direction (optional)
        horMagnitude: Pandas series or array of floats
            if U and V are not given, then give horMagnitude
        readData: Boolean
            if passing data instead of fieldnames, set this to False.



        Returns
        -------
        offAxisAngel: Pandas Series or Array

        """
        if not horMagnitude:
            horMagnitude = self.compute_horizontal_wind_magnitude(U,V,readData)

        if readData:
            W = self.reader.get_timeseries(W,self.startDate,self.endDate)

        offAxisAngle = 90 - np.arctan(horMagnitude.values,W.values)*180/np.pi

        return offAxisAngle

    def compute_welch_spectra(self,measure,fs,readData=True,alpha=0.49,nu=1.608*10**(-5),C=0.008,**kwargs):
        """
        Computes the power spectral density of power spectrum of wind speed (measure)

        Parameters
        ----------
        measure: Str or array of floats
            Wind speed to compute welch spectra
        fs: float
            sampling frequency of the measure time series in units of Hz
        **kwargs: key arguments
            any key arguments that the scipy.signal.welch function takes

        Returns
        -------
        dict:
            waveNumber: ndarray
                array of wavenumbers
            spectrum: ndarray
                Power spectral density of power spectrum of measure
            epsilon: float
            l_k: float
            lambda_g: float

        """
        from scipy.signal import welch
        if readData:
            measure = self.reader.get_timeseries(measure,self.startDate,self.endDate)
        
        freq,dens = welch(measure,fs,**kwargs)
        waveNumber = freq/np.mean(measure)
        spectrum = dens*np.mean(measure)

        epsilon = (np.mean(measure)*C/alpha)**(3/2)
        l_k = 1000*(nu**3/epsilon)**(1/4)
        lambda_g = 1000*np.sqrt(15*nu*np.std(measure)/epsilon)

        return {'waveNumber':waveNumber,'spectrum':spectrum,'epsilon':epsilon,\
                'l_k':l_k,'lambda_g':lambda_g}
