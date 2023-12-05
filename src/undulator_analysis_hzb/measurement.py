'''
Created on Oct 16, 2023

@author: oqb
'''
import importlib.resources
import numpy as np
import undulator_analysis_hzb.track as trk
import datetime as dt
from tarfile import grp
import scipy.interpolate as interp
from scipy import signal

class measurement(object):
    '''
    This class contains all of the data of a 'measurement', and the methods to analyse and summarise the measurement.
    
    
    '''
    def __init__(self, measurement_name, **kwargs):
        '''
        The constructor method.
        
        Variables
        ---------
        measurement_name (str)
        '''
        self.name = measurement_name
        for key, value in kwargs.items():
            self.__setattr__(key, value)
            
        self.measurement_system = None
        
        self.processed = False # attribute to quickly indicate if base data has been processed (Volts to B)
        
        self.analysed = False # attribute to quickly indicate if processed data has been post-processed (1st, 2nd integrals, phase etc)
        
    def __repr__(self):
        return 'Measurement()'
    
    def __str__(self):
        #TODO tidy up print command
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
    """
    A class to describe measurements from the HZB Granite Messbank.
    """
    
    def __init__(self, measurement_name, **kwargs):
        """Constructor for granite_bank_measurement.
        
        Date 5.12.23:
        
        The Granite Messbank in the the Schwerlasthalle is the primary measurement
        system for 3D field mapping at Helmholtz-Zentrum Berlin. It takes a measurement
        along the longitudinal axis X, and that axis can be positioned in the 
        vertical (Y) and transverse (Z) directions. These are relative positions.
        
        Parameters
        ----------
        measurement : `measurement`
            This class is subclassed from `measurement`
            
        Attributes
        ----------
        measurement_name : str
            The name of the measurement. Often a number as a string.
            
        Other Parameters
        ----------------
        measurement_timestamp : datetime object
            The timestamp of the measurement.
        """
        super(granite_bank_measurement,self).__init__(measurement_name)
        #self.name = measurement_name
        
        for key, value in kwargs.items():
            self.__setattr__(key, value)
    
    #TODO Technical Details in init
    
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
                
                #rescue divide by zero errors when making scales
                if float(self.x_step) == 0:
                    self.x_step =1
            
            if loglines[line][0:17] == 'Y AXIS  Parameter':
                self.y_start = float(loglines[line+1].split()[-1])
                self.y_end = float(loglines[line+2].split()[-1])
                self.y_step = float(loglines[line+3].split()[-1])
                self.y_velocity = float(loglines[line+5].split()[-1])
                self.y_return_velocity = float(loglines[line+6].split()[-1])
                self.y_unit = 'mm'
                
                #rescue divide by zero errors when making scales
                if float(self.y_step) == 0:
                    self.y_step =1
                
            if loglines[line][0:17] == 'Z AXIS  Parameter':
                self.z_start = float(loglines[line+1].split()[-1])
                self.z_end = float(loglines[line+2].split()[-1])
                self.z_step = float(loglines[line+3].split()[-1])
                self.z_velocity = float(loglines[line+5].split()[-1])
                self.z_return_velocity = float(loglines[line+6].split()[-1])
                self.z_unit = 'mm'
                
                #rescue divide by zero errors when making scales
                if float(self.z_step) == 0:
                    self.z_step =1
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
        #TODO pull track reading out from metadata function!
        pass
    
    def process_measurement(self):
        """An instance method to process the raw DVM data to B Fields
        
        Expanded text. 
        
        Modifies main_x_range, B_array and processed
        
        Uses tracks and measurement_system
        
        Returns
        -------
        self.B_array : numpy.ndarray
            The processed DVM array as a B_array.
        self.main_x_range : numpy.ndarray
            The main x range of the processed B array.
        self.processed : bool
            The 'has this measurement been processed' variable.
        """
        
        #create interpolation of y,z calib curves
        interpy = interp.CubicSpline(self.measurement_system.y_calib_senis[:,0],
                                     self.measurement_system.y_calib_senis[:,1])
        interpz = interp.CubicSpline(self.measurement_system.z_calib_senis[:,0],
                                     self.measurement_system.z_calib_senis[:,1])
        
        
        #from collection of B fields,find the maximum 'min',
        mins = np.array([])
        maxs = np.array([])
        for trac in self.tracks:
            mins = np.append(mins, np.min(self.tracks[trac].dvm_data[:,0]))
            maxs = np.append(maxs, np.max(self.tracks[trac].dvm_data[:,0]))
            
        print ('mins: {} \n maxs: {}'.format(mins,maxs))
        #and the minimum 'max' of our x range
        
        #find central track (or nominate primary track)
        
        trac = 1222
        
        #interpolates the central DVM track. This should be a function in track.py
        u, c = np.unique(self.tracks[trac].dvm_data[:,0], return_index = True)
        interpdvmy = interp.CubicSpline(self.tracks[trac].dvm_data[c,0],
                                        self.tracks[trac].dvm_data[c,1])
        small_step = 0.05
        x_scale = np.arange(np.min(self.tracks[trac].dvm_data[:,0]),
                            np.max(self.tracks[trac].dvm_data[:,0]),
                            small_step)
        dvm_x = interpdvmy(x_scale)
        
        #find peaks
        dvm_x_peaks = signal.find_peaks(np.abs(dvm_x), height = 0.95*np.max(dvm_x))
        #find central peak
        dvm_x_peaks_centre_ind = int(np.floor((dvm_x_peaks[0].__len__()+1)/2))
        #location of central peak
        x_mid = x_scale[dvm_x_peaks[0][dvm_x_peaks_centre_ind]]
        x_mid_round = np.round(x_mid,2)
        #find number of periods
        num_periods = dvm_x_peaks[0].__len__()/2
        
        #find undulator period length
        period_power = np.argmax(np.abs(np.fft.fft(dvm_x[dvm_x_peaks[0][0]:dvm_x_peaks[0][-1]])))
        period_len_calc = small_step*1/np.fft.fftfreq(dvm_x[dvm_x_peaks[0][0]:dvm_x_peaks[0][-1]].__len__())[period_power]
        #
        
        #create a nice regular grid to interpolate on
        period_len_round = np.round(period_len_calc,1)
        #centre - period_length*((periods/2)+6)
        grid_min = x_mid_round - period_len_round*((num_periods/2)+6)
        grid_max = x_mid_round + period_len_round*((num_periods/2)+6)
        #check min is within all ranges
        #check max is within all ranges
        while grid_min < np.min(mins) and grid_max > np.max(maxs):
            grid_min += period_len_round
            grid_max -= period_len_round
            
        #create B array
        self.main_x_range = np.arange(grid_min, grid_max, period_len_calc/20)
        DVM_array = np.zeros([self.main_x_range.__len__(),1,3,2])
        self.B_array = np.zeros([self.main_x_range.__len__(),1,3,2]) #calculate 1 and 3
        #then do interpolations!
        i = 0
        #for track in tracks
        for trac in self.tracks:
            #rebase measurement
            DVM_array[:,0,i,:] = self.tracks[trac].rebase_track(self.main_x_range)
            
            i+=1
        #create B fields
        self.B_array[:,:,:,0] = interpy(DVM_array[:,:,:,0])
        self.B_array[:,:,:,1] = interpz(DVM_array[:,:,:,1])
        print('to here')
        
        
        
        #interpolate B fields and produce single B array
        #save B array as attribute of self
        
        #assign 'processed' attribute as True
        self.processed = True
        
        return self.B_array, self.main_x_range, self.processed
        
        
    #Saving stuff to measurement group
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
            #save the B_array data
            elif item == 'B_array':
                #requires dataset
                grp.require_dataset('{}'.format(item),  shape = self.__getattribute__(item).shape, dtype = self.__getattribute__(item).dtype)
                #this overwrites the existing dataset. It *should* be the same, but it's unsafe I guess
                #TODO fix this overwriting issue
                grp[item][...] = self.__getattribute__(item)
                grp[item].attrs['unit'] = 'T'
                
            else:
                print(item)
                grp.attrs[item] = self.__getattribute__(item)
        
        for track in self.tracks:
            #are you sure you need to create another group here?
            trk = grp.require_group('{}'.format(track))
            trk.require_dataset('{}'.format(track), shape = self.tracks[track].dvm_data.shape, dtype = self.tracks[track].dvm_data.dtype)
            
            trk[str(track)][...] = self.tracks[track].dvm_data
            trk[str(track)].attrs['unit'] = 'V'
            #TODO don't forget to build up metadata as attributes
            
            print (trk)
            
        print(grp)
    
        if 'B_array' in grp:
            #append dimensions and attributes
            
            #create x_axis dataset
            grp.require_dataset('x_axis', shape = self.main_x_range.shape, dtype = self.main_x_range.dtype)
            grp['x_axis'][...] = self.main_x_range
            grp['x_axis'].make_scale('Longitudinal Axis')
            grp['x_axis'].attrs['unit'] = 'mm'
            
            #attach x-axis
            grp['B_array'].dims[0].label = 'x'
            grp['B_array'].dims[0].attach_scale(grp['x_axis'])
            
            #create y_axis dataset
            yax = np.linspace(self.y_start, self.y_end, int(1+(self.y_end-self.y_start)/self.y_step))
            grp.require_dataset('y_axis', shape = yax.shape, dtype = yax.dtype)
            grp['y_axis'][...] = yax
            grp['y_axis'].make_scale('Vertical Axis')
            grp['y_axis'].attrs['unit'] = 'mm'
            
            #attach y-axis
            grp['B_array'].dims[1].label = 'y'
            grp['B_array'].dims[1].attach_scale(grp['y_axis'])
            
            #create z_axis dataset
            zax = np.linspace(self.z_start, self.z_end, int(1+(self.z_end-self.z_start)/self.z_step))
            grp.require_dataset('z_axis', shape = zax.shape, dtype = zax.dtype)
            grp['z_axis'][...] = zax
            grp['z_axis'].make_scale('Transverse Axis')
            grp['z_axis'].attrs['unit'] = 'mm'
            
            #attach z-axis
            grp['B_array'].dims[2].label = 'z'
            grp['B_array'].dims[2].attach_scale(grp['z_axis'])
            
            #create B_orientation dataset
            # Bax = np.array(['By', 'Bz'], dtype = object)
            # grp.require_dataset('B_orientation', shape = (2,), dtype = object)
            # grp['B_orientation'][...] = Bax
            # grp['B_orientation'].make_scale('B_orientation')
            #
            # #attach B_orientation
            # grp['B_array'].dims[3].label = 'B'
            # grp['B_array'].dims[3].attach_scale(grp['B_orientation'])
            #

            
            
##area for custom exception
class IncompleteMetadataError(Exception):
    def __init__(self,message):
#        m = ''
#        for elem in missing_metadata:
#            m += elem + ', '
#        message = 'This measurement is missing the metadata for {}'.format(m[:-2])
        super().__init__(message)
        #can this error later highlight the missing boxes??