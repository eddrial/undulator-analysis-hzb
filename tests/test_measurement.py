'''
Created on Jan 18, 2024

@author: oqb
'''
import pytest
import os
import undulator_analysis_hzb.track as trk
import undulator_analysis_hzb.campaign as cmp
import undulator_analysis_hzb.measurement_system as ms
import importlib.resources
import numpy as np

#fixtures
file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/test_campaign.h5')
data_comparison_folder = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/08.02.2022')

x_file = importlib.resources.files('undulator_analysis_hzb').joinpath('../../resources/x_calib_senis112_17.spl')
y_file = importlib.resources.files('undulator_analysis_hzb').joinpath('../../resources/y_calib_senis112_17.spl')
z_file = importlib.resources.files('undulator_analysis_hzb').joinpath('../../resources/z_calib_senis112_17.spl')

granite_messbank = ms.Measurement_System("Granite_Messbank")
granite_messbank.load_hall_calibration_files(x_file, y_file, z_file)

mc = cmp.Campaign(file_path, campaign_name = 'camp_test')

@pytest.fixture
def my_campaign():
    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/test_campaign.h5')
    mc = cmp.Campaign(file_path)
    
    return mc

class TestConstructor():
    
    def test_constructor(self, my_campaign):
        assert my_campaign.filepath == file_path