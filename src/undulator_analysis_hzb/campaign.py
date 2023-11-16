'''
Created on Oct 26, 2023

@author: oqb
'''

import os
import h5py as h5
import undulator_analysis_hzb.track as trk
from undulator_analysis_hzb.measurement import measurement

class Campaign(object):
    '''This is the top level class allowing access to all 
    data and metadata of a measurement campaign, from component magnet blocks
    through to final device'''
    def __init__(self,filepath,**kwargs):
        self.filepath = filepath
        
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        #self.campaign_name = campaign_name
        
        #setting up multi-level dictionary writing
        self.data_store = {}
    
        '''        self.structure = {'Component':
                          {'Ident':
                           {'Step':
                            {'State':
                             {'Measurement':
                              {'Track':{}
                               }
                              }
                             }
                            }
                           }
                          }
                          '''
        
        self.structure = {}
    
    
    ###I/O functions
    def create_campaign_file(self):
    
        try:
            h5.File(self.filepath,'w-')
        except:
            print('{} exists. Open the file or choose a different name.'.format(self.filepath))
                
        else:
            h5.File(self.filepath,'w-')
    
    def load_campaign_file(self):
        pass
    
    def save_campaign_file(self):
        pass
        
    ### Adding and Manipulation of Measurement objects to Campaign
        
    def add_measurement (self, measurement):
        #measurement must contain certain attributes to allow it to be placed in campaign structure
        #required attributes
        #component, ident, step, state?, measurement_system, measurement_timestamp
        #optional attributes
        #author, comment
        try:
            measurement.check_metadata()
        except Exception as e:
            print (e.args[0])
        
        else:
            print ('The measurement has all the required metadata')
            
            if measurement.component not in self.data_store.keys():
                self.data_store[measurement.component] = {}
                
            if measurement.ident not in \
                self.data_store[measurement.component].keys():
                
                self.data_store[measurement.component] \
                                [measurement.ident] = {}
                                
            if measurement.step not in \
                self.data_store[measurement.component] \
                                [measurement.ident].keys():
                self.data_store[measurement.component] \
                                [measurement.ident] \
                                [measurement.step]= {}
                                
            if measurement.state not in \
                self.data_store[measurement.component] \
                                [measurement.ident] \
                                [measurement.step].keys():
                self.data_store[measurement.component] \
                                [measurement.ident] \
                                [measurement.step] \
                                [measurement.state]= {}
            
            self.data_store[measurement.component] \
                            [measurement.ident] \
                            [measurement.step] \
                            [measurement.state] \
                            ['measurement'] = measurement
                    
#

    
        