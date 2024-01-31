'''
Created on Oct 26, 2023

@author: oqb
'''

import undulator_analysis_hzb.campaign as cmp
import undulator_analysis_hzb.track as trk
import undulator_analysis_hzb.measurement as mes
import undulator_analysis_hzb.measurement_system as ms
import importlib.resources
from undulator_analysis_hzb.measurement import granite_bank_measurement
import numpy as np
import matplotlib.pyplot as plt
import pathlib

if __name__ == '__main__':
    
    
    
# Place to store and work with the hdf5 file
    file_path = pathlib.WindowsPath('D:/Work - Laptop/UE51/UE51 Measurements/UE51.h5')

#name the campaign
    a = cmp.Campaign(file_path, campaign_name = 'UE51')
    
#create the campaign data file
    a.create_campaign_file()

    
    #a.add_track(my_track)
    
    print (a.campaign_name)
    
    #generating measurement
    b = mes.measurement('RUN1277')

    #file path to the Log file
    lfile_path = pathlib.WindowsPath('D:/Work - Laptop/UE51/UE51 Measurements/Measurement 8/RUN1277.LOG')
    #debug statement
    print(b.__class__)
    
    #create the measurement type to a granite messbank measurement
    granite_bank_measurement.convert_to_granite_bank_measurement(b)
    
    #debug statements
    print(b.__class__)
    print (b.name)
    b.define_logfile(lfile_path)
    
    
    #Hall Probe Calibration Files
    x_file = importlib.resources.files('undulator_analysis_hzb').joinpath('../../resources/x_calib_senis112_17.spl')
    y_file = importlib.resources.files('undulator_analysis_hzb').joinpath('../../resources/y_calib_senis112_17.spl')
    z_file = importlib.resources.files('undulator_analysis_hzb').joinpath('../../resources/z_calib_senis112_17.spl')
    
    #create the measurement system and add the granite messbank
    granite_messbank = ms.Measurement_System("Granite_Messbank")
    granite_messbank.load_hall_calibration_files(x_file, y_file, z_file)
    
    #read the logfile and add metadata to the measurement
    b.read_logfile_metadata()
    
    #define the component identity tree
    b.add_component('Whole_Undulator')
    b.add_ident('1')
    b.add_state('G20S0')
    b.add_step('Step_8')
    b.add_measurement_system(granite_messbank)
    
    #process the measurement
    b.process_measurement()
    #analyse the measurement
    b.analyse_measurement()
    #add the measurement to the campaign
    a.add_measurement(b)
    
    
#    a.add_measurement_system(granite_messbank)


    a.save_campaign_file()
    a.save_measurement_system_to_file()
    print(b.logfile)