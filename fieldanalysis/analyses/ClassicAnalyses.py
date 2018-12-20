#!/usr/bin/env python
"""
Created : 06-12-2018
Last Modified : Wed 19 Dec 2018 07:18:06 PM EST
Created By : Enrique D. Angola
"""
import pandas as pd
import numpy as np

class ClassicAnalyses():

    """


    Parameters
    ----------


    Returns
    -------


    Examples
    --------
    >>>

    """

    def __init__(self,reader=None,startDate = None, endDate = None):
        self.reader = reader
        self.startDate = startDate
        self.endDate = endDate

    def compute_ws_ratio(self,anem1=None,anem2=None):

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

        TI = 100*np.mean(anemSD/anemAvg)

        return TI


    def compute_binned_TI(self,anemAvg,anemSD,bins,binBy):
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
            binnedTI.append(self.compute_TI(dataAvg,dataSD,False))


        return binnedTI

    def compute_binned_bias(self,sensor1,sensor2,bins,binBy,meanBias = True):
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


    def compute_linear_regression(self,measure1,measure2,readData=True):
        """


        Parameters
        ----------


        Returns
        -------


        """
        from sklearn import datasets, linear_model
        from sklearn.metrics import mean_squared_error, r2_score

        if readData:
            measure1 = self.reader.get_timeseries(measure1,self.startDate,self.endDate)
            measure2 = self.reader.get_timeseries(measure2,self.startDate,self.endDate)

        r = np.corrcoef(measure1,measure2)[0,1] #correlation coefficient

        measure1 = measure1.reshape(len(measure1),1)
        measure2 = measure2.reshape(len(measure2),1)

        regr = linear_model.LinearRegression()

        regr.fit(measure1,measure2)
        params = (regr.coef_[0],regr.intercept_)

        predict = regr.predict(measure1)
        r2 = r2_score(measure2,predict) #coefficient of determination, explained variance
        mse = mean_squared_error(measure2,predict)

        return {'params':params,'r2':r2,'mse':mse, 'r':r}

