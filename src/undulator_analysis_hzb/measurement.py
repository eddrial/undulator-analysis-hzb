'''
Created on Oct 16, 2023

@author: oqb
'''

import numpy as np
import undulator_analysis_hzb.track as trk

class measurement(object):
    '''
    classdocs
    '''
    def __init__(self, measurement_name):
        '''
        Constructor
        '''
        self.name = measurement_name
        
        
#        print('a useless line that is different again')
        
    def define_logfile(self,logfile_path):
        self.logfile = logfile_path
        
    
class granite_bank_measurement(measurement):
    def __init__(self, measurement_name):
        super(granite_bank_measurement,self).__init__(measurement_name)
    
    @classmethod
    def convert_to_granite_bank_measurement(cls,obj):
        obj.__class__ = granite_bank_measurement
        
    
    def read_logfile_metadata(self):
        f = open(self.logfile, 'r')
        self.loglines = f.readlines()
        print ('log data read into self.loglines')
        