'''
Created on Oct 26, 2023

@author: oqb
'''

import undulator_analysis_hzb.campaign as cmp
import undulator_analysis_hzb.track as trk
import undulator_analysis_hzb.measurement as mes
import importlib.resources
from undulator_analysis_hzb.measurement import granite_bank_measurement


if __name__ == '__main__':
    
    
    
    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/test_campaign.h5')
    
    a = cmp.Campaign(file_path, campaign_name = 'UE51')
    
    a.create_campaign_file()
    
    my_track = trk.track()
    my_track.load_dvm_data(file_path)
    
    my_track.component = 'Girder'
    my_track.part = 'Upper'
    my_track.state = 'nullshift'
    my_track.step = 0
    my_track.measurement = '01'
    
    a.add_track(my_track)
    
    print (a.name)
    
    #generating measurement
    b = mes.measurement('RUN1221')
    lfile_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/RUN1221.LOG')
    
    print(b.__class__)
    
    granite_bank_measurement.convert_to_granite_bank_measurement(b)
    
    print(b.__class__)
    print (b.name)
    b.define_logfile(lfile_path)
    
    b.read_logfile_metadata()
    
    print(b.loglines)