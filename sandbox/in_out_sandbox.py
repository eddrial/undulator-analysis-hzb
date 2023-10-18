'''
Created on Oct 16, 2023

@author: oqb
'''
import importlib.resources
import numpy as np
from undulator_analysis_hzb import data_io as dio

if __name__ == '__main__':
    file_path_dvm = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
    file_path_mag = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/HP-FIELD1221.DAT')
    file_path_log = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/RUN1221.LOG')
    
    
    io_object_dvm = dio.data_io(file_path_dvm)
    io_object_mag = dio.data_io(file_path_mag)
    
    
    a = io_object_dvm.open()
    b = io_object_mag.open()
        
        
    print(a.shape)
    print(b.shape)