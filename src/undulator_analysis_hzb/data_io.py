'''
Created on Oct 16, 2023

@author: oqb
'''
import numpy as np

class data_io(object):
    '''
    classdocs
    '''


    def __init__(self, file_path):
        '''
        Constructor
        '''
        self.file_path = file_path
        self.file_type = file_path.name.partition('.')[-1]
        
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
            
#        print('a useless line that is different again')
        
    def open(self):
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
