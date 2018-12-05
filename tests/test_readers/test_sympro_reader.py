#!/usr/bin/env python
"""
Created : 04-12-2018
Last Modified : Wed 05 Dec 2018 03:05:23 PM EST
Created By : Enrique D. Angola
"""

from fieldanalysis.readers.SymPro import SymPro as reader

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
