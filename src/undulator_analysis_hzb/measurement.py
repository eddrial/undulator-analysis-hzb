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
import scipy.integrate as integ
from scipy import signal
from scipy import constants as cnst

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
        self.tracks = {}
        for i in range(int((self.z_end-self.z_start)/self.z_step)+1):
            self.tracks[int(self.name[3:])+i] = trk.track()
        
        for trac in self.tracks:
            
            file_path_dvm = self.logfile.parent.joinpath('./MAG{}.DVM'.format(trac))
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
        
        trac = min(self.tracks)+int((len(self.tracks)+1)/2)
        
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
        self.period_power = np.argmax(np.abs(np.fft.fft(dvm_x[dvm_x_peaks[0][0]:dvm_x_peaks[0][-1]])))
        self.period_len_calc = small_step*1/np.fft.fftfreq(dvm_x[dvm_x_peaks[0][0]:dvm_x_peaks[0][-1]].__len__())[self.period_power]
        #
        
        #create a nice regular grid to interpolate on
        self.period_len_round = np.round(self.period_len_calc,1)
        #centre - period_length*((periods/2)+6)
        grid_min = x_mid_round - self.period_len_round*((num_periods/2)+6)
        grid_max = x_mid_round + self.period_len_round*((num_periods/2)+6)
        #check min is within all ranges
        #check max is within all ranges
        while grid_min < np.min(mins) and grid_max > np.max(maxs):
            grid_min += self.period_len_round
            grid_max -= self.period_len_round
            
        #create B array
        self.main_x_range = np.arange(grid_min, grid_max, self.period_len_round/600)
        y_tracks = int(1+(self.y_end-self.y_start)/self.y_step)
        z_tracks = int(1+(self.z_end-self.z_start)/self.z_step)
        DVM_array = np.zeros([self.main_x_range.__len__(),y_tracks,z_tracks,2])
        self.B_array = np.zeros([self.main_x_range.__len__(),y_tracks,z_tracks,2]) 
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
        
        #average peak B
        self.B0 = interpz(np.mean(dvm_x_peaks[1]['peak_heights']))
        
        #average K value
        self.K = cnst.e*self.B0*self.period_len_round*1e-3/(2*np.pi*cnst.c *cnst.m_e)
        
        #locations of peaks of By in x (real undulator, do I need this?)
        self.B_peaks_x = signal.find_peaks(np.abs(self.B_array[:,int(y_tracks/2),int(z_tracks/2),0]), height = 0.95*np.max(self.B_array))
        
        
        print('to here')
        
        
        
        #interpolate B fields and produce single B array
        #save B array as attribute of self
        
        #assign 'processed' attribute as True
        self.processed = True
        
        return self.B_array, self.main_x_range, self.processed
        
    def analyse_measurement(self, 
                            calc_F = True, 
                            calc_S = True,
                            calc_T = True,
                            calc_Phi = True):
        """An instance method to analyse processed B Fields.
        
        This method is a collection of other methods to analyse the 
        measured B field and produce:
        
        First Field Integrals
        Second Field Integrals
        Trajectory
        Phase Error  
        
        Parameters
        ----------
        calc_F : bool
            A boolean switch to call the first field integral calculation
        calc_F : bool
            A boolean switch to call the second field integral calculation
        calc_F : bool
            A boolean switch to call the trajectory calculation
        calc_Phi : bool
            A boolean switch to call the phase error calculation   
            
        Returns
        -------
        self.analysed : bool
            A boolean to identify if the measurement has been 'fully' analysed
        """
        
        #switch to calculate first integral
        if calc_F == True:
            self.calculate_I1()
            
        if calc_S == True:
            self.calculate_I2()
            
        if calc_T == True:
            self.calculate_trajectory()
            #TODO self.calculate_trajectory()
            pass
        
        if calc_Phi == True:
            #TODO self.calculate_phase_error()
            self.calculate_phase_error()
        
        if np.all([calc_F, calc_S, calc_T, calc_Phi] ) == True:
            self.analysed = True
        
        return self.analysed
    
    def calculate_I1(self):
        """An instance method to calculate the first integral from I1 array.
        
        This basically then a wrapper for numpy.cumsum. Multiplies by step in main_x_range.
        
        Returns
        -------
        self.i2 : np.ndarray
            The second integral array. The same shape as B_array
        """
        print('I am calculating I1')
        self.I1 = (self.main_x_range[2]-self.main_x_range[1])*np.cumsum(self.B_array[:,:,:,:], axis = 0)
        
        self.I1_trap = integ.cumulative_trapezoid(self.B_array[:,:,:,:], self.main_x_range, axis = 0, initial = 0.0)
        
        return self.I1
        
    def calculate_I2(self):
        """An instance method to calculate the second integral from the first integral.
        
        This basically then a wrapper for numpy.cumsum. Multiplies by step in main_x_range.
        
        Returns
        -------
        self.i1 : np.ndarray
            The first integral array. The same shape as B_array
        """
        print('I am calculating I2')
        self.I2 = (self.main_x_range[2]-self.main_x_range[1])*np.cumsum(self.I1[:,:,:,:], axis = 0)
        self.I2_trap = integ.cumulative_trapezoid(self.I1_trap[:,:,:,:], self.main_x_range, axis = 0, initial = 0.0)
        
        return self.I2
    
    def calculate_trajectory(self):
        """An instance method to calculate the trajectory from the 2nd integral.
        
        The force on the electron due to the B field is F = q(v x B), 
        which can relate to the second derivative of position through F = m.d2x/dt2.
        The second integral has already been calculated.
        Just multiplied through by q/(gamma.m.v)
        
        v = c.sqrt(1-(1/(1+e.V/(mc^2))^2))
        
        Returns
        -------
        self.i1 : np.ndarray
            The first integral array. The same shape as B_array
            
        References
        ----------
        https://www.slac.stanford.edu/pubs/slactns/tn04/slac-tn-10-076.pdf
        """
        print('I am calculating trajectory')
        Ebessy = 1.7e9 #TODO needs to be in Messbank
        gamma = Ebessy/511000
        v = cnst.c * np.sqrt(1-(1/(1+cnst.e*Ebessy/(cnst.m_e*cnst.c**2))**2))
        self.trajectory = self.I2*1e-6*cnst.e/(gamma * v * cnst.m_e)
        
        return self.trajectory
        
    def calculate_phase_error(self):
        print('I am calculating phase error')
        Ebessy = 1.7e9
        gamma = Ebessy/511000
        
        beta = np.sqrt(1-(1/(1+cnst.e*Ebessy/(cnst.m_e*cnst.c**2))**2))
        
        #This is deflection in radians
        #Int[0,L]Bydz = theta*(gamma*m*c^2)/e*c
        defl = self.I1*1e-3*cnst.e/(beta*gamma*cnst.m_e*cnst.c)

#        self.nom_peaks = np.arange(self.B_peaks_x[0][79]-300*79,self.B_peaks_x[0][79]+300*78, 300 )
            
        phijintegrand = integ.cumulative_trapezoid((gamma*beta*defl[:,int(defl.shape[1]/2),int(defl.shape[2]/2),0])**2\
                                                   +(gamma*beta*defl[:,int(defl.shape[1]/2),int(defl.shape[2]/2),1])**2, self.main_x_range*1e-3, initial = 0)\
                    -self.main_x_range*1e-3*self.K**2/2
                    
        phijconsts = (2*np.pi/self.period_len_calc)/(1 + self.K**2/2)
        
        phij_rad = phijconsts*phijintegrand
        
        phij_deg = phij_rad*360/(2*np.pi)
        #I think I'm close with phij_deg. maybe a factor 10 out. But the maths is there? Is it?
                    
        
        print('wait here')
        
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