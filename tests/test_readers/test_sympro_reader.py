#!/usr/bin/env python
"""
Created : 04-12-2018
Last Modified : Thu 27 Dec 2018 12:26:29 PM EST
Created By : Enrique D. Angola
"""

from fieldanalysis import readers
from pytest import approx
import pandas as pd

class TestSymproReader():

    def setup(self):
        filename = 'tests/testfiles/symprotest.txt'
        self.object = readers.SymPro(filename)

    def test_get_data_dataSuccesfullyRead_returnsTrue(self):

        valueOne = int(self.object.get_data('Ch1_Anem_58.00m_E_Avg_m/s').iloc[0])
        valueLast = int(self.object.get_data('Ch1_Anem_58.00m_E_Avg_m/s').iloc[-1])

        assert valueOne == 7 and valueLast == 7

    def test_get_fieldnames_properLengthFieldnames_returnsTrue(self):

        fieldnames = self.object.get_fieldnames()
        assert len(fieldnames) == 109

    def test_get_fieldnames_properFirstAndLast_returnsTrue(self):

        fieldnames = self.object.get_fieldnames()
        assert fieldnames[0] == 'Timestamp' and\
                fieldnames[-1] == 'Ch26_Vane_57.00m_S_GustDir_deg'

    def test_get_timeseries_properShape_returnsTrue(self):

        timeseries = self.object.get_timeseries('Ch1_Anem_58.00m_E_Gust_m/s',\
                '2018-06-22 00:00:00','2018-06-22 00:20:00')

        assert timeseries.shape == (3,)

    def test_get_timeseries_properDates_returnsTrue(self):

        timeseries = self.object.get_timeseries('Ch1_Anem_58.00m_E_Gust_m/s',\
                '2018-06-22 00:00:00','2018-06-22 00:20:00')

        assert timeseries.index[0] == pd.Timestamp('2018-06-22 00:00:00') and \
                timeseries.index[-1] == pd.Timestamp('2018-06-22 00:20:00')

    def test_get_timeseries_firstAndLastValues_returnsTrue(self):

        timeseries = self.object.get_timeseries('Ch1_Anem_58.00m_E_Gust_m/s',\
                '2018-06-22 00:00:00','2018-06-22 00:20:00')

        assert timeseries.iloc[0] == approx(8.72,0.01) and \
                timeseries.iloc[-1] == approx(8.68,0.01)

    def test_apply_filter_filteredDataframe_returnsTrue(self):

        from fieldanalysis.filters import ClassicFilters as cf
        filters = cf(self.object)
        filters.generate_icing_filter(temp='Ch17_Analog_2.00m_S_Avg_C',\
                vaneSD='Ch26_Vane_57.00m_S_SD_deg')
        self.object.apply_filters(filters)

        assert self.object.data.shape == (4,109)

    def test_apply_filter_filteredDataFilteredTimestamp_returnsTrue(self):

        from fieldanalysis.filters import ClassicFilters as cf
        filters = cf(self.object)
        filters.generate_icing_filter(temp='Ch17_Analog_2.00m_S_Avg_C',vaneSD='Ch26_Vane_57.00m_S_SD_deg')
        self.object.apply_filters(filters)

        assert self.object.data.Timestamp.iloc[-1] == '2018-06-22 00:30:00'

    def test_remove_filters_retrieveOriginalData_returnsTrue(self):

        from fieldanalysis.filters import ClassicFilters as cf
        filters = cf(self.object)
        filters.generate_icing_filter(temp='Ch17_Analog_2.00m_S_Avg_C',vaneSD='Ch26_Vane_57.00m_S_SD_deg')
        self.object.apply_filters(filters)
        self.object.remove_filters()
        assert self.object.data.Timestamp.iloc[-1] == '2018-11-14 23:50:00' and\
                self.object.data.shape == (5,109)

    def test_get_fieldname_returnProperFieldname_returnsTrue(self):

        fieldname = self.object.get_fieldname('Ch1','Avg')

        assert fieldname == 'Ch1_Anem_58.00m_E_Avg_m/s'

    def test_get_height_returnPoperHeight_returnsTrue(self):

        height = self.object.get_height(22)

        assert height == '20.00'
