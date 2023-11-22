'''
Created on Oct 16, 2023

@author: oqb
'''
import pytest
import undulator_analysis_hzb.track as trk
import importlib.resources
import numpy as np

#fixtures
@pytest.fixture
def my_track():
    a = trk.track()
    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
    a.load_dvm_data(file_path)
    return a

class TestConstructor():
    
    def test_created(self, my_track):
        assert my_track.track_name == '1221'
        
class TestTrackLoading():

    def test_load_dvm_data_file_type(self,my_track):
        
        assert my_track.file_type == 'DVM'
        
    def test_open_dvm(self, my_track):
        assert my_track.dvm_data.shape == (5150,3)

