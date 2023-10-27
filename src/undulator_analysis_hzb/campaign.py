'''
Created on Oct 26, 2023

@author: oqb
'''
import h5py as h5
import undulator_analysis_hzb.track as trk

class Campaign(object):
    '''This is the top level class allowing access to all 
    data and metadata of a measurement campaign, from component magnet blocks
    through to final device'''
    def __init__(self,campaign_name):
        self.campaign_name = campaign_name
        
        self.data_store = {}
    
        '''        self.structure = {'Component':
                          {'Part':
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
        self.name = campaign_name
        
        self.structure = {}

    def add_track(self,track):
        if track.component not in self.data_store.keys():
            self.data_store[track.component] = {}
        
        if track.part not in self.data_store[track.component].keys():
            self.data_store[track.component][track.part] = {}
            
        if track.step not in self.data_store[track.component]\
                                            [track.part].keys():
            self.data_store[track.component]\
            [track.part]\
            [track.step] = {}
            
        if track.state not in self.data_store[track.component]\
                                            [track.part]\
                                            [track.step].keys():
            self.data_store[track.component]\
            [track.part]\
            [track.step]\
            [track.state] = {}
            
        if track.measurement not in self.data_store[track.component]\
                                            [track.part]\
                                            [track.step]\
                                            [track.state].keys():
            self.data_store[track.component]\
            [track.part]\
            [track.step]\
            [track.state]\
            [track.measurement] = {}
            
        if track.track_name not in self.data_store[track.component]\
                                            [track.part]\
                                            [track.step]\
                                            [track.state]\
                                            [track.measurement].keys():
            self.data_store[track.component]\
            [track.part]\
            [track.step]\
            [track.state]\
            [track.measurement]\
            [track.track_name] = {}
            
        if 'DVMData' not in self.data_store[track.component]\
                                            [track.part]\
                                            [track.step]\
                                            [track.state]\
                                            [track.measurement]\
                                            [track.track_name].keys():
            self.data_store[track.component]\
            [track.part]\
            [track.step]\
            [track.state]\
            [track.measurement]\
            [track.track_name]\
            ['DVMData'] = track.dvm_data
#                                track.state:
#                                    track.measurement:
#                                        track.name:
#                                            'DVMData'} = track.dvm_data