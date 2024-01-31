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


if __name__ == '__main__':
    
    
    
    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/UE56_sesa_campaign.h5')
    
#    a = cmp.Campaign(file_path, campaign_name = 'UEtest')
    a = cmp.Campaign(file_path, campaign_name = 'UE56_SESA')
    
    a.create_campaign_file()
    
    my_track = trk.track()
    my_track.load_dvm_data(file_path)
    
    my_track.component = 'Girder'
    my_track.part = 'Upper'
    my_track.state = 'nullshift'
    my_track.step = 0
    my_track.measurement = '01'
    
    #a.add_track(my_track)
    
    print (a.campaign_name)
    
    #generating measurement
    b = mes.measurement('RUN601')
    #lfile_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/RUN1221.LOG')
    lfile_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/08.02.2022/complete_map/RUN601.LOG')
    #Run 601 equates to phase measurement...
    print(b.__class__)
    
    granite_bank_measurement.convert_to_granite_bank_measurement(b)
    
    print(b.__class__)
    print (b.name)
    b.define_logfile(lfile_path)
    
    
    
    x_file = importlib.resources.files('undulator_analysis_hzb').joinpath('../../resources/x_calib_senis112_17.spl')
    y_file = importlib.resources.files('undulator_analysis_hzb').joinpath('../../resources/y_calib_senis112_17.spl')
    z_file = importlib.resources.files('undulator_analysis_hzb').joinpath('../../resources/z_calib_senis112_17.spl')
    
    granite_messbank = ms.Measurement_System("Granite_Messbank")
    granite_messbank.load_hall_calibration_files(x_file, y_file, z_file)
    
    b.read_logfile_metadata()
    
    b.add_component('A_Component')
    b.add_ident('An_Ident')
    b.add_state('A_State')
    b.add_step('Step_X')
    b.add_measurement_system(granite_messbank)
    
    b.process_measurement()
    b.analyse_measurement()
    a.add_measurement(b)
    
    
#    a.add_measurement_system(granite_messbank)

    proc1221 = np.genfromtxt('HP-FIELD1221.DAT',skip_header = 1)
    proc1222 = np.genfromtxt('HP-FIELD1222.DAT',skip_header = 1)
    proc1223 = np.genfromtxt('HP-FIELD1223.DAT',skip_header = 1)
    
#    plt.plot(b.main_x_range,b.I2[:,0,1,0])
#    plt.plot(proc1222[:,0],proc1222[:,5])
    plt.plot(b.main_x_range, b.trajectory[:,0,1,0])
    plt.show(block = 1)
 
 
    
    a.save_campaign_file()
    a.save_measurement_system_to_file()
    print(b.logfile)