#!/usr/bin/env python

from fieldanalysis import filters
from fieldanalysis import readers

class TestClassicFilters():

    def setup(self):
        filename = 'tests/testfiles/symprotest.txt'
        self.reader = readers.SymPro(filename)
        self.object = filters.ClassicFilters(self.reader)

    def test_generate_icing_filter_checkFirstAndLastIcing_returnsTrue(self):

        self.object.generate_icing_filter(temp='Ch17_Analog_2.00m_S_Avg_C',\
                vaneSD='Ch26_Vane_57.00m_S_SD_deg')
        
        icingFilter = self.object.filtersDict['icing']

        assert not icingFilter.iloc[-1]
        assert icingFilter.iloc[0]
