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
    a = trk.track('0001')
    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
    a.load_dvm_data(file_path)
    return a

class TestConstructor():
    
    def test_created(self, my_track):
        assert my_track.track_number == '0001'
        
class TestTrackType():
#    a = trk.track('0001')
#    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
#    a.load_dvm_data(file_path)
    def test_load_dvm_data_file_type(self,my_track):
        
        assert my_track.file_type == 'DVM'
'''        
    def test_dat(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/HP-FIELD1221.DAT')
        assert dio.data_io(file_path).file_type == 'DAT'

class TestOpen():
    
    def test_open_dvm(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
        file_object = dio.data_io(file_path)
        assert file_object.open().shape == (5150,3)
        
    def test_self_dvm(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
        file_object = dio.data_io(file_path)
        file_object.open()
        assert file_object.dvm_data.shape == (5150,3)
        
    def test_open_dat(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/HP-FIELD1221.DAT')
        file_object = dio.data_io(file_path)
        assert file_object.open().shape == (5148,7)
        
    def test_self_dat(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/HP-FIELD1221.DAT')
        file_object = dio.data_io(file_path)
        file_object.open()
        assert file_object.proc_data.shape == (5148,7)
        
    
    def test_self_xy(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/HP-FIELD1221.DAT')
        file_object = dio.data_io(file_path)
        file_object.open()
        #assert file_object.yz == np.array([-5.,0.])
        np.testing.assert_array_equal(file_object.yz, np.array([0,-5]))'''
        