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
        
    def create_campaign_file(self):
    
        try:
            h5.File(self.filepath,'w-')
        except:
            print('{} exists.'.format(self.filepath))
                
        else:
            h5.File(self.filepath,'w-')
    
    def load_campaign_file(self):
        pass
    
    def save_campaign_file(self):
        pass
        

#    def add_component(self,component):
#        self.__setattr__('component', component)
        
#    def add_ident(self,ident):
#        self.__setattr__('ident', ident)
    
        