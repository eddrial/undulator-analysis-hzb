'''
Created on Oct 19, 2023

@author: oqb
'''

import importlib.resources
import numpy as np
from undulator_analysis_hzb import data_io as dio
from undulator_analysis_hzb import field_analysis as fa

if __name__ == '__main__':
    file_path_dvm = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
    file_path_mag = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/HP-FIELD1221.DAT')
    
    this_dvm = dio.data_io(file_path_dvm)
    
    this_dvm.open()
    
    