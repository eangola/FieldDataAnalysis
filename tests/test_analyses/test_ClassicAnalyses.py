#!/usr/bin/env python
"""
Created : 11-12-2018
Last Modified : Fri 28 Dec 2018 05:15:40 PM EST
Created By : Enrique D. Angola
"""
from fieldanalysis import readers
from fieldanalysis import analyses
from pytest import approx
class TestClassicAnalyses():

    def setup(self):
        filename = 'tests/testfiles/symprotest.txt'
        reader = readers.SymPro(filename)
        self.object = analyses.ClassicAnalyses(reader)

    def test_ws_ratio_checkFirstAndLastRatio_returnsTrue(self):

        ratio = self.object.compute_ws_ratio('Ch1_Anem_58.00m_E_Avg_m/s','Ch2_Anem_50.00m_E_Min_m/s')
        assert int(ratio[0]) == 1 and int(ratio[3]) == 1

    def test_ws_ratio_checkLength_returnsTrue(self):

        ratio = self.object.compute_ws_ratio('Ch1_Anem_58.00m_E_Avg_m/s','Ch2_Anem_50.00m_E_Min_m/s')
        assert len(ratio) == 5

    def test_bin_data_valueReturn_returnsTrue(self):

        bins = [7,7.5,7.9]
        group = self.object._bin_data('Ch1_Anem_58.00m_E_Avg_m/s',bins,'Ch1_Anem_58.00m_E_Avg_m/s')
        elements = []
        for key in group.groups:
            elements.append(group.get_group(key))
        
        assert elements[0].values[0] <= bins[1] and elements[0].values[1] <= bins[1]
        assert elements[1].values[1] >= bins[1]
        assert elements[0].shape == (2,) and elements[1].shape == (3,)
