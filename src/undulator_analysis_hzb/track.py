'''
Created on Oct 16, 2023

@author: oqb
'''
import numpy as np
import scipy.interpolate as interp

class track(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
#        print('a useless line that is different again')
        
    def load_dvm_data(self, file_path):
        self.file_path = file_path
        self.file_type = file_path.name.partition('.')[-1]
        self.track_name = file_path.name.partition('.')[-3][-4:]
        
        #determine file type and describe file
        if self.file_type == 'DVM':
            self.file_description = '''A Digital Volt Meter output file.
            Contains x-axis (mm) ¦ Voltmeter Reading (V) ¦ Standard deviation (V)'''
        
        elif self.file_type == 'DAT':
            self.file_description = '''Should be a file containing processed DVM data to magnetic field data.
            First Line Y (mm) ¦ Z (mm)
            Then X (mm) ¦ Field Y (T) ¦ Field Z (T) ¦ 1st Int Y (Tmm) ¦ 1st Int Z (Tmm) ¦ 2nd Int Y (Tmm2) ¦ 2nd Int Z (Tmm2)'''
        
        elif self.file_type == 'LOG':
            self.file_description = '''A Log file for a collection set. Contains Log Info in a standard format'''    
        
        elif self.file_type == 'h5':
            self.file_description = '''An HDF5 file gathering all data together in a self descriptive way'''    
            
            
        #open track data depending on type
        if self.file_type == 'DVM':
            self.dvm_data = np.genfromtxt(self.file_path)
            
            return self.dvm_data
        
        if self.file_type == 'DAT':
            self.proc_data = np.genfromtxt(self.file_path, skip_header = 1)
            with open(self.file_path) as f:
                yz = f.readline()
            yz = yz.split()
            yz[0] = float(yz[0])
            yz[1] = float(yz[1])
            self.yz = np.array(yz)
            return self.proc_data
        
        if self.file_type == 'h5':
            pass
        
    def process_track(self, meas_system):
        """
        This function processes a raw track from a measurement bench to a B field.
        
        This function creates an interpolation function for the y and z hall probes
        and calculates the B field. 
        1st Column of dvm_data is Position (x)
        2nd column of dvm_data is Voltage from vertical Hall Probe (Vy)
        3rd column of dvm_data is Voltage from horizontal Hall Probe (Vz).
        """
        #TODO How to know if it's a Granite Messbank Track, instead of any track?
        
        print('processing....')
        #create a spline fit function for x/y/z
        
        #build new path from spline
        interpy = interp.CubicSpline(meas_system.y_calib_senis[:,0],meas_system.y_calib_senis[:,1])
        interpz = interp.CubicSpline(meas_system.z_calib_senis[:,0],meas_system.z_calib_senis[:,1])
        
        By = interpy(self.dvm_data[:,1])
        Bz = interpz(self.dvm_data[:,2])
        
        B_processed = np.array([self.dvm_data[:,0],By,Bz])
        
        return B_processed
    
    def rebase_track(self,x_axis_array):
        #find indices of unique distances
        u, c = np.unique(self.dvm_data[:,0], return_index = True)
        interpDVM1 = interp.CubicSpline(self.dvm_data[c,0],self.dvm_data[c,1])
        interpDVM2 = interp.CubicSpline(self.dvm_data[c,0],self.dvm_data[c,2])
        
        rebase_DVM = np.zeros([x_axis_array.__len__(),2])
        rebase_DVM[:,0] = interpDVM1(x_axis_array)
        rebase_DVM[:,1] = interpDVM2(x_axis_array)
        
        return rebase_DVM