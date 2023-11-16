'''
Created on Oct 26, 2023

@author: oqb
'''

import os
import h5py as h5
import undulator_analysis_hzb.track as trk

class Campaign(object):
    '''This is the top level class allowing access to all 
    data and metadata of a measurement campaign, from component magnet blocks
    through to final device'''
    def __init__(self,filepath,**kwargs):
        self.filepath = filepath
        
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        #self.campaign_name = campaign_name
        
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
        except:
            print ('Metadata from measurement missing. Please fill all attributes.')
        
        print ('this is the end of the function add_measurement')

#    def add_component(self,component):
#        self.__setattr__('component', component)
        
#    def add_ident(self,ident):
#        self.__setattr__('ident', ident)
    
        