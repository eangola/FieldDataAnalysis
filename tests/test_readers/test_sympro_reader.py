#!/usr/bin/env python
"""
Created : 04-12-2018
Last Modified : Thu 06 Dec 2018 12:48:12 PM EST
Created By : Enrique D. Angola
"""

from fieldanalysis.readers import SymPro as reader

class TestSymproReader():

    def setup(self):
        filename = 'tests/testfiles/symprotest.txt'
        self.object = reader(filename)

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

    def test_get_timeseries_properShapre_returnsTrue(self):

        timeseries = self.object.get_timeseries('Ch1_Anem_58.00m_E_Gust_m/s',\
                '2018-06-22 00:00:00','2018-06-22 00:20:00')

        assert timeseries.shape == (3,2)

    def test_apply_filter_filteredDataframe_returnsTrue(self):

        from fieldanalysis.filters import classic_filters as cf
        filters = cf(self.object)
        filters.generate_icing_filter(temp='Ch17_Analog_2.00m_S_Avg_C',vaneSD='Ch26_Vane_57.00m_S_SD_deg')
        self.object.apply_filters(filters)

        assert self.object.data.shape == (4,109)
