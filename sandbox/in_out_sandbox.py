'''
Created on Oct 16, 2023

@author: oqb
'''
import importlib.resources
import numpy as np
from undulator_analysis_hzb import data_io as dio

if __name__ == '__main__':
    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
    
    io_object = dio.data_io(file_path)
    
    with open(file_path) as f:
        a = np.genfromtxt(f)
        
        
    print(a.shape)