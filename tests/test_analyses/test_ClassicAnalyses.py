#!/usr/bin/env python
"""
Created : 11-12-2018
Last Modified : Tue 11 Dec 2018 04:36:10 PM EST
Created By : Enrique D. Angola
"""
from fieldanalysis import readers
from fieldanalysis import analyses
class TestClassicAnalyses():

    def setup(self):
        filename = 'tests/testfiles/symprotest.txt'
        reader = readers.SymPro(filename)
        self.object = analyses.ClassicAnalyses(reader)

    def test_ws_ratio_checkFirstAndLastRatio_returnsTrue(self):

        ratio = self.object.ws_ratio('Ch1_Anem_58.00m_E_Avg_m/s','Ch2_Anem_50.00m_E_Min_m/s')
        assert int(ratio[0]) == 1 and int(ratio[3]) == 1

    def test_ws_ratio_checkLength_returnsTrue(self):

        ratio = self.object.ws_ratio('Ch1_Anem_58.00m_E_Avg_m/s','Ch2_Anem_50.00m_E_Min_m/s')
        assert len(ratio) == 5
