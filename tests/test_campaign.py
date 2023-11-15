'''
Created on Oct 16, 2023

@author: oqb
'''
import pytest
import os
import undulator_analysis_hzb.track as trk
import undulator_analysis_hzb.campaign as cmp
import importlib.resources
import numpy as np

#fixtures
file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/test_campaign.h5')


@pytest.fixture
def my_campaign():
    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/test_campaign.h5')
    mc = cmp.Campaign(file_path)
    
    return mc

class TestConstructor():
    
    def test_constructor(self, my_campaign):
        assert my_campaign.filepath == file_path
        
    def test_constructor_with_kwargs(self):
        mc = cmp.Campaign(file_path, campaign_name = 'camp_test')
        assert mc.campaign_name == 'camp_test'
        
class TestFileIO():
    
    def test_create_campaign_file(self,my_campaign):
        my_campaign.create_campaign_file()
        assert os.path.exists(my_campaign.filepath) == True
        
        
class TestTrackLoading():

    def test_load_dvm_data_file_type(self,my_track):
        
        assert my_track.file_type == 'DVM'
        
    def test_open_dvm(self, my_track):
        assert my_track.dvm_data.shape == (5150,3)

