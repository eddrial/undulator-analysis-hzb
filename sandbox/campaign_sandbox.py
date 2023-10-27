'''
Created on Oct 26, 2023

@author: oqb
'''

import undulator_analysis_hzb.campaign as cmp
import undulator_analysis_hzb.track as trk
import importlib.resources


if __name__ == '__main__':
    a = cmp.Campaign(campaign_name = 'UE51')
    
    my_track = trk.track()
    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG1221.DVM')
    my_track.load_dvm_data(file_path)
    
    my_track.component = 'Girder'
    my_track.part = 'Upper'
    my_track.state = 'nullshift'
    my_track.step = 0
    my_track.measurement = '01'
    
    a.add_track(my_track)
    
    print (a.name)
    