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
    
    
    
    file_path = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/UE56_sesa_campaign_bspl.h5')
    
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
    # plt.plot(b.main_x_range, b.trajectory[:,0,1,0])
    # plt.show(block = 1)
    
    #a lot of this should move into testing somehow
    #comparisons against Analyze produced data
    
    main_path = 'C:/Users/oqb/dawn-workspace/undulator_analysis_hzb/tests/resources/08.02.2022/complete_map/mult10b'
    #DVM
    mult10bydvm = np.genfromtxt('{}y.dvm'.format(main_path))
    mult10bzdvm = np.genfromtxt('{}z.dvm'.format(main_path))
    
    # dvm_diff_plot = plt.plot((b.tracks[610].dvm_data[:,0:3:2]-mult10bzdvm)[:,0])
    # dvm_diff_plot.title('Difference in X position in X range between .dvm and .hdf5')
    # dvm_diff_plot.xlabel('Position n')
    # dvm_diff_plot.ylabel('Variation (mm)')
    
    #CAL
    mult10bycal = np.genfromtxt('{}y.cal'.format(main_path))
    mult10bzcal = np.genfromtxt('{}z.cal'.format(main_path))
    
    plt.plot(mult10bycal[:,0],mult10bycal[:,1], label = '.cal data')
    plt.plot(b.main_x_range,b.B_array[:,0,9,0], label = '.hdf5 interpolated data')
    # cal_diff_plot.legend()
    # cal_diff_plot.title('Difference between .cal and .hdf5 files')
    # cal_diff_plot.xlabel('X (mm)')
    # cal_diff_plot.ylabel('Field (T)')
    
    #SPL
    mult10byspl = np.genfromtxt('{}y.spl'.format(main_path))
    mult10bzspl = np.genfromtxt('{}z.spl'.format(main_path))
    
    plt.plot(mult10byspl[:,0], mult10byspl[:,1])
    plt.plot(mult10bycal[:,0], mult10bycal[:,1])
    plt.plot(b.main_x_range,b.B_array[:,0,9,0])
    plt.plot(b.main_x_range,b.B_array_bg_subtracted[:,0,9,0])
    
    #SPI
    mult10byspi = np.genfromtxt('{}y.spi'.format(main_path))
    mult10bzspi = np.genfromtxt('{}z.spi'.format(main_path))
    
    plt.plot(mult10byspi[:,0], mult10byspi[:,1])
    plt.plot(mult10bzspi[:,0], mult10bzspi[:,1])
#    plt.plot(b.main_x_range,b.I1[:,0,9,0])
    plt.plot(b.main_x_range,b.I1_trap[:,0,9,0])
#    plt.plot(b.main_x_range,b.I1[:,0,9,1])
    plt.plot(b.main_x_range,b.I1_trap[:,0,9,1])
    
    #SII
    mult10bysii = np.genfromtxt('{}y.sii'.format(main_path))
    mult10bzsii = np.genfromtxt('{}z.sii'.format(main_path))
    
    plt.plot(mult10bysii[:,0], mult10bysii[:,1])
    plt.plot(mult10bzsii[:,0], mult10bzsii[:,1])
#    plt.plot(b.main_x_range,b.I2[:,0,9,0])
    plt.plot(b.main_x_range,b.I2_trap[:,0,9,0])
    plt.plot(b.main_x_range,b.I2_trap_bg[:,0,9,0])
#    plt.plot(b.main_x_range,b.I2[:,0,9,1])
    plt.plot(b.main_x_range,b.I2_trap[:,0,9,1])
    plt.plot(b.main_x_range,b.I2_trap_bg[:,0,9,1])
    
    #PHA
    mult10bypha = np.genfromtxt('{}y.pha'.format(main_path))
    mult10bzpha = np.genfromtxt('{}z.pha'.format(main_path))
    
    plt.plot(mult10bypha[:,0], mult10bypha[:,1])
    plt.plot(mult10bzpha[:,0], mult10bzpha[:,1])
    
    a.save_campaign_file()
    a.save_measurement_system_to_file()
    print(b.logfile)