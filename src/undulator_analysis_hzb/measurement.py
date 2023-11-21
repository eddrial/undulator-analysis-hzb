'''
Created on Oct 16, 2023

@author: oqb
'''
import importlib.resources
import numpy as np
import undulator_analysis_hzb.track as trk
import datetime as dt
from tarfile import grp

class measurement(object):
    '''
    classdocs
    '''
    def __init__(self, measurement_name, **kwargs):
        '''
        Constructor
        '''
        self.name = measurement_name
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        
        print('a useless line that is different again')
        
    def __repr__(self):
        return 'Measurement()'
    
    def __str__(self):
        #TODO tidy up pront command
        return 'Measurement: {}'.format(self.name)

    def add_component(self,component):
        #TODO look at making series of component classes? But a string descriptor will do
        self.__setattr__('component', component)
        
    def add_ident(self,ident):
        #just a string
        self.__setattr__('ident', ident)

    def add_step(self,step):
        #which step of the measurement?
        self.__setattr__('step', step)

    def add_state(self,state):
        #dictionary - that ties into component class?
        self.__setattr__('state', state)
        
    def add_measurement_system(self,measurement_system):
        self.__setattr__('measurement_system', measurement_system)



    def check_metadata(self):
        required_metadata = ['component',
                             'ident',
                             'step',
                             'state',
                             'measurement_timestamp',
                             'measurement_system']
        missing_metadata = []
        
        for attrib in required_metadata:
            if attrib not in self.__dict__:
                missing_metadata.append(attrib)
        
        if missing_metadata.__len__() > 0:
            message = ''
            for elem in missing_metadata:
                message += elem + ', '
            message = 'This measurement is missing the metadata for {}'.format(message[:-2])
 
            raise IncompleteMetadataError(message)
            print('1')

        else:
            return True
        
        
    def define_logfile(self,logfile_path):
        self.logfile = logfile_path
        
    
class granite_bank_measurement(measurement):
    def __init__(self, measurement_name, **kwargs):
        super(granite_bank_measurement,self).__init__(measurement_name)
        self.name = measurement_name
        
        for key, value in kwargs.items():
            self.__setattr__(key, value)
    
    def __repr__(self):
        return 'GraniteBankMasurement()'
    
    @classmethod
    def convert_to_granite_bank_measurement(cls,obj):
        obj.__class__ = granite_bank_measurement
        
    
    def read_logfile_metadata(self):
        f = open(self.logfile, 'r')
        loglines = f.readlines()
        print ('log data read into loglines')
        
        for line in range(len(loglines)):
            if loglines[line][0:4] == 'Date':
                self.measurement_timestamp = dt.datetime.strptime(loglines[line].split()[1] +
                                                                  ' ' +
                                                                  loglines[line].split()[2],'%d-%b-%y %H:%M:%S')
            
#            if loglines[line].split()[0] == 'Operator:':
#                self.operator = loglines[line].split()[1]
            
            if loglines[line][0:17] == 'X AXIS  Parameter':
                self.x_start = float(loglines[line+1].split()[-1])
                self.x_end = float(loglines[line+2].split()[-1])
                self.x_step = float(loglines[line+3].split()[-1])
                self.x_velocity = float(loglines[line+5].split()[-1])
                self.x_return_velocity = float(loglines[line+6].split()[-1])
                self.x_unit = 'mm'
            
            if loglines[line][0:17] == 'Y AXIS  Parameter':
                self.y_start = float(loglines[line+1].split()[-1])
                self.y_end = float(loglines[line+2].split()[-1])
                self.y_step = float(loglines[line+3].split()[-1])
                self.y_velocity = float(loglines[line+5].split()[-1])
                self.y_return_velocity = float(loglines[line+6].split()[-1])
                self.y_unit = 'mm'
                
            if loglines[line][0:17] == 'Z AXIS  Parameter':
                self.z_start = float(loglines[line+1].split()[-1])
                self.z_end = float(loglines[line+2].split()[-1])
                self.z_step = float(loglines[line+3].split()[-1])
                self.z_velocity = float(loglines[line+5].split()[-1])
                self.z_return_velocity = float(loglines[line+6].split()[-1])
                self.z_unit = 'mm'
                
            if loglines[line][0:16] == 'Pitch  Parameter':
                self.pitch_start = float(loglines[line+1].split()[-1])
                self.pitch_end = float(loglines[line+2].split()[-1])
                self.pitch_step = float(loglines[line+3].split()[-1])
                self.pitch_velocity = float(loglines[line+5].split()[-1])
                self.pitch_return_velocity = float(loglines[line+6].split()[-1])
                self.pitch_unit = 'deg'
        
        #TODO actually algorithmically derive Track Numbers
        self.tracks = {1221:trk.track(), 1222: trk.track(), 1223: trk.track()}
        
        for trac in self.tracks:
            
            file_path_dvm = importlib.resources.files('undulator_analysis_hzb').joinpath('../../tests/resources/MAG{}.DVM'.format(trac))
            self.tracks[trac].load_dvm_data(file_path_dvm)
                
    def read_tracks(self):
        pass
    
    def save_measurement_group(self,grp):
        for item in self.__dict__:
            if item == 'measurement_system':
                pass
            elif item == 'tracks':
                pass
            elif item == 'logfile':
                pass
            elif item == 'measurement_timestamp':
                pass
            else:
                print(item)
                grp.attrs[item] = self.__getattribute__(item)
        
        for track in self.tracks:
            trk = grp.create_group('{}'.format(track))
            trk.create_dataset('{}'.format(track), data = self.tracks[track].dvm_data)
            #TODO don't forget to build up metadata as attributes
            
            print (trk)
            
        print(grp)
    
    
    
##area for custom exception
class IncompleteMetadataError(Exception):
    def __init__(self,message):
#        m = ''
#        for elem in missing_metadata:
#            m += elem + ', '
#        message = 'This measurement is missing the metadata for {}'.format(m[:-2])
        super().__init__(message)
        #can this error later highlight the missing boxes??