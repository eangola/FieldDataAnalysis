#!/usr/bin/env python
"""
Created : 04-12-2018
Last Modified : Tue 04 Dec 2018 06:03:31 PM EST
Created By : Enrique D. Angola
"""

from fieldanalysis.readers.SymPro import SymPro as reader

class TestSymproReader():

    def setup(self):
        filename = 'tests/testfiles/symprotest.txt'
        self.object = reader(filename)

    def test_read_data_dataSuccesfullyRead_returnsTrue(self):

        self.object.read_data()
        data = self.object.data

        valueOne = int(data['Ch1_Anem_58.00m_E_Avg_m/s'].iloc[0])
        valueLast = int(data['Ch1_Anem_58.00m_E_Avg_m/s'].iloc[-1])

        assert valueOne == 7 and valueLast == 7
