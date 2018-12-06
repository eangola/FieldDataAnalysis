#!/usr/bin/env python

from fieldanalysis.filters import classic_filters as cf
from fieldanalysis.readers import SymPro

class TestClassicFilters():

    def setup(self):
        filename = 'tests/testfiles/symprotest.txt'
        reader = SymPro(filename)
        self.object = cf(reader)

    def test_generate_icing_filter_checkFirstAndLast_returnsTrue(self):

        self.object.generate_icing_filter(temp='Ch17_Analog_2.00m_S_Avg_C',\
                vaneSD='Ch26_Vane_57.00m_S_SD_deg')
        filtersList = list(self.object.filtersDict.values())[0]

        assert filtersList[4] == False and filtersList[0] == True
