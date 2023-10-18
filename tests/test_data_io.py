'''
Created on Oct 16, 2023

@author: oqb
'''
#   import unittest
import pytest
#import undulator_analysis_hzb.demo1 as demo1
from undulator_analysis_hzb import data_io as dio
import importlib.resources


class TestConstructor():
    
    def test_dvm(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
        assert dio.data_io(file_path).file_type == 'DVM'
        
    def test_log(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/RUN1221.LOG')
        assert dio.data_io(file_path).file_type == 'LOG'
        
    def test_dat(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/HP-FIELD1221.DAT')
        assert dio.data_io(file_path).file_type == 'DAT'

class TestOpen():
    
    def test_open_dvm(self):
        file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
        file_object = dio.data_io(file_path)
        assert file_object.open().shape == (5150,3)
        
        