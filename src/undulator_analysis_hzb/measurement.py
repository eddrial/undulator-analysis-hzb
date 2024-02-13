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
import matplotlib.pyplot as plt

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
        
        #find central track (or nominate primary track) - what is actually going on here?
        #does not nee to be done on trac... can be  done from interpolated B0....no?
        #finding #periods, period length and B0 and K
        
        trac = min(self.tracks)+int((len(self.tracks)+1)/2)
        #from here each track needs its own information, for phase error calculation etc
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
        ####UNTIL HERE
        #from here each track needs its own information, for phase error calculation etc
        #interpolates the central DVM track. This should be a function in track.py
        #sorts out the array into unique elements
        for trac in self.tracks:
            self.tracks[trac].u, self.tracks[trac].c = np.unique(self.tracks[trac].dvm_data[:,0], return_index = True)
            self.tracks[trac].interpdvmy = interp.CubicSpline(self.tracks[trac].dvm_data[self.tracks[trac].c,0],
                                            self.tracks[trac].dvm_data[self.tracks[trac].c,1])
            #where can this be parameterised?
            small_step = 0.05
            x_scale = np.arange(np.min(self.tracks[trac].dvm_data[:,0]),
                                np.max(self.tracks[trac].dvm_data[:,0]),
                                small_step)
            self.tracks[trac].dvm_x = self.tracks[trac].interpdvmy(x_scale)
            
            #find peaks
            self.tracks[trac].dvm_x_peaks = signal.find_peaks(np.abs(dvm_x), height = 0.95*np.max(self.tracks[trac].dvm_x))
            #find central peak
            self.tracks[trac].dvm_x_peaks_centre_ind = int(np.floor((self.tracks[trac].dvm_x_peaks[0].__len__()+1)/2))
            #location of central peak
            self.tracks[trac].x_mid = x_scale[dvm_x_peaks[0][dvm_x_peaks_centre_ind]]
            self.tracks[trac].x_mid_round = np.round(x_mid,2)
            #find number of periods
            self.tracks[trac].num_periods = self.tracks[trac].dvm_x_peaks[0].__len__()/2
            
            #find undulator period length
            self.tracks[trac].period_power = np.argmax(np.abs(np.fft.fft(self.tracks[trac].dvm_x[self.tracks[trac].dvm_x_peaks[0][0]:self.tracks[trac].dvm_x_peaks[0][-1]])))
            self.tracks[trac].period_len_calc = np.abs(small_step*1/np.fft.fftfreq(self.tracks[trac].dvm_x[self.tracks[trac].dvm_x_peaks[0][0]:self.tracks[trac].dvm_x_peaks[0][-1]].__len__())[self.tracks[trac].period_power])
            #
        ####UNTIL HERE
        
        period_len_calc_tmp = np.zeros(len(self.tracks))
        for i in range(len(self.tracks)): 
            period_len_calc_tmp[i] = self.tracks[trac].period_len_calc
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
        
        
        #remove background
        #TODO actually read in from some external source
        self.backgrBY = np.array([-2.5e-005, -2.9e-005])  #UE56 SESAME Testing
        self.backgrBZ = np.array([0.7e-6,  4.5e-6])   #UE56 SESAME testing
#        self.backgrBY = np.array([-1.7e-005, -2.9e-005])  #UE51 SESAME Testing
#        self.backgrBZ = np.array([1.0e-6,  12e-6])   #UE51 testing
        
        self.B_array_bg_subtracted = np.zeros(self.B_array.shape)
        
        #for each track in B Array
        #    first element = is - soll
        #    last element  - ist - soll
        
        for trak in range(self.B_array.shape[2]):
            sub_to_background_BY_ar =  np.linspace(self.B_array[0,0,trak,0]-self.backgrBY[0],self.B_array[-1,0,trak,0]-self.backgrBY[1], num = self.B_array.shape[0], endpoint = True)
            sub_to_background_BZ_ar =  np.linspace(self.B_array[0,0,trak,1]-self.backgrBZ[0],self.B_array[-1,0,trak,1]-self.backgrBZ[1], num = self.B_array.shape[0], endpoint = True)
        
        #self.backgrBY_ar = np.linspace(self.backgrBY[0],self.backgrBY[1], num = self.B_array.shape[0], endpoint = True)
        #self.backgrBZ_ar = np.linspace(self.backgrBZ[0],self.backgrBZ[1], num = self.B_array.shape[0], endpoint = True)
        
            a = np.vstack([sub_to_background_BY_ar,sub_to_background_BZ_ar])
        
            self.B_array_bg_subtracted[:,:,trak,:] = self.B_array[:,:,trak,:]-a[:, None, :].T
        
        self.B_array_bg_subtracted_peaks = {}
        self.num_periods_array = np.zeros(self.B_array.shape[2])
        self.period_len_round_array = np.zeros(self.B_array.shape[2])
        self.period_len_calc_array = np.zeros(self.B_array.shape[2])
        self.period_len_round_array = np.zeros(self.B_array.shape[2])
        self.B0_array = np.zeros(self.B_array.shape[2])
        self.K_calc_array = np.zeros(self.B_array.shape[2])
        #calculate period lengths
        for i in range(self.B_array.shape[2]):
            
            self.B_array_bg_subtracted_peaks[i] = signal.find_peaks(np.abs(self.B_array_bg_subtracted[:,0,i,0]), height = 0.95*np.max(self.B_array_bg_subtracted[:,0,i,0]))
        #calculate period #
            self.num_periods_array[i] = self.B_array_bg_subtracted_peaks[i][0].__len__()/2
        #average peak B for each row row
            period_power = np.argmax(np.abs(np.fft.fft(self.B_array_bg_subtracted[self.B_array_bg_subtracted_peaks[i][0][0]:self.B_array_bg_subtracted_peaks[i][0][-1],0,i,0])))
            period_len_calc = np.abs((self.main_x_range[1]-self.main_x_range[0])*1/np.fft.fftfreq(self.B_array_bg_subtracted[self.B_array_bg_subtracted_peaks[i][0][0]:self.B_array_bg_subtracted_peaks[i][0][-1],0,i,0].__len__())[period_power])
            
            self.period_len_calc_array[i] = period_len_calc
            self.period_len_round_array[i] = np.round(period_len_calc,1)
            
            self.B0_array[i] = interpy(np.mean(self.B_array_bg_subtracted_peaks[i][1]['peak_heights']))
            self.K_calc_array[i] = cnst.e*self.B0_array[i]*self.period_len_round_array[i]*1e-3/(2*np.pi*cnst.c *cnst.m_e)
        self.B0 = interpy(np.mean(dvm_x_peaks[1]['peak_heights']))
        
        
        
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
            self.calculate_phase_error_array()
            print('pause here end of phase calculation')
        
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
        #self.I1 = (self.main_x_range[2]-self.main_x_range[1])*np.cumsum(self.B_array[:,:,:,:], axis = 0)
        
        self.I1_trap = integ.cumulative_trapezoid(self.B_array[:,:,:,:], self.main_x_range, axis = 0, initial = 0.0)
        
        self.I1_trap_bg = integ.cumulative_trapezoid(self.B_array_bg_subtracted[:,:,:,:], self.main_x_range, axis = 0, initial = 0.0)
        return self.I1_trap
        
    def calculate_I2(self):
        """An instance method to calculate the second integral from the first integral.
        
        This basically then a wrapper for numpy.cumsum. Multiplies by step in main_x_range.
        
        Returns
        -------
        self.i1 : np.ndarray
            The first integral array. The same shape as B_array
        """
        print('I am calculating I2')
#        self.I2 = (self.main_x_range[2]-self.main_x_range[1])*np.cumsum(self.I1[:,:,:,:], axis = 0)
        self.I2_trap = integ.cumulative_trapezoid(self.I1_trap[:,:,:,:], self.main_x_range, axis = 0, initial = 0.0)
        self.I2_trap_bg = integ.cumulative_trapezoid(self.I1_trap_bg[:,:,:,:], self.main_x_range, axis = 0, initial = 0.0)
        
        return self.I2_trap
    
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
        self.trajectory = self.I2_trap*1e-6*cnst.e/(gamma * v * cnst.m_e)
        
        return self.trajectory
        
    def calculate_phase_error(self):
        print('I am calculating phase error')
        #phi_j = ((2pi/lambda_u)/(1+K^2/2))int[0,z_j](gamma^2*beta_T^2(z)-K^2/2)dz
        #this clearly needs improving, because must be independent of machine!
        #energy of BESSY - probably doesn't want to be in this part
        Ebessy = 1.7e9
        #the gamma of BESSY
        gamma = Ebessy/511000
        
        #Average velocity of electron
        beta = np.sqrt(1-(1/(1+cnst.e*Ebessy/(cnst.m_e*cnst.c**2))**2))
        
        #This is deflection in radians in our given machine, BESSY
        defl = self.I1_trap*1e-3*cnst.e/(beta*gamma*cnst.m_e*cnst.c)
        #transverse velocity beta_t
        beta_t = beta * np.sqrt(defl[:,:,:,0]**2 + defl[:,:,:,1]**2) 
        #reduce X range from first to last pole and integrate the path.
        X = self.main_x_range[self.B_peaks_x[0][0]:self.B_peaks_x[0][-1]+1]
        #integrate the integrand gamma^2*beta_T^2 over reduced range
        Y = integ.cumulative_trapezoid(gamma**2*beta_t[self.B_peaks_x[0][0]:self.B_peaks_x[0][-1]+1,0,15]**2,self.main_x_range[self.B_peaks_x[0][0]:self.B_peaks_x[0][-1]+1],initial = 0)
        
        #fit the resulting integrand
        fit = np.polyfit(X, Y, 1)
        #create the fit function
        linear_baseline = np.poly1d(fit) # create the linear baseline function
        
        #this subtracts the integrated K^2/2
        new_Y = Y-linear_baseline(X)
        #plt.plot(X[(self.B_peaks_x[0]-self.B_peaks_x[0][0])[0:-1]],new_Y[(self.B_peaks_x[0]-self.B_peaks_x[0][0])[0:-1]])
        
        #this again gives the positions of the poles. perhaps unnecessary
        j_poles = X[(self.B_peaks_x[0]-self.B_peaks_x[0][0])[0:-1]]
        
        #phase error all the way through the device
        self.phase = new_Y
        
        #phase error at each pole. plots what I would normally expect
        self.phase_j = new_Y[(self.B_peaks_x[0]-self.B_peaks_x[0][0])[0:-1]]
        
        #determine local K from slope
        loc_K = np.sqrt(2*linear_baseline[1])
        
        #these are the constants from the front of the equation
        phijconsts = (2*np.pi/self.period_len_calc)/(1 + loc_K**2/2)
        
        #take the mean of the collection
        local_phase_error_rad = np.mean(phijconsts*np.abs(self.phase_j))
        
        #multiply up to degrees
        self.local_phase_error_deg = local_phase_error_rad*180/np.pi
        
        print('local phase error is {}'.format(self.local_phase_error_deg))
        
        print('wait here')
        
        return self.local_phase_error_deg

    def calculate_phase_error_array(self):
        print('I am calculating phase error')
        #phi_j = ((2pi/lambda_u)/(1+K^2/2))int[0,z_j](gamma^2*beta_T^2(z)-K^2/2)dz
        #this clearly needs improving, because must be independent of machine!
        #energy of BESSY - probably doesn't want to be in this part
        Ebessy = 1.7e9
        #the gamma of BESSY
        gamma = Ebessy/511000
        
        #Average velocity of electron
        beta = np.sqrt(1-(1/(1+cnst.e*Ebessy/(cnst.m_e*cnst.c**2))**2))
        
        #This is deflection in radians in our given machine, BESSY. All trajecotries OK
        defl = self.I1_trap*1e-3*cnst.e/(beta*gamma*cnst.m_e*cnst.c)
        #transverse velocity beta_t. All trajectories OK.
        beta_t = beta * np.sqrt(defl[:,:,:,0]**2 + defl[:,:,:,1]**2)
        
        self.phase_error_array_rms = np.zeros(beta_t.shape[1:])
        self.loc_K = np.zeros(beta_t.shape[1:])
        phijconsts = np.zeros(beta_t.shape[1:])
        local_phase_error_rad_array = np.zeros(beta_t.shape[1:])
        self.local_phase_error_deg_array = np.zeros(beta_t.shape[1:])
        self.phase_error_array = {}
        self.phase_error_array_j = np.zeros(((self.B_array_bg_subtracted_peaks[0][0]-self.B_array_bg_subtracted_peaks[0][0][0])[0:-1].__len__(),
                                            beta_t.shape[1],
                                            beta_t.shape[2]))
        
        
        #reduce X range from first to last pole and integrate the path.
        for i in range(self.phase_error_array_j.shape[2]):
            X = self.main_x_range[self.B_array_bg_subtracted_peaks[i][0][0]:self.B_array_bg_subtracted_peaks[i][0][-1]+1]
        #integrate the integrand gamma^2*beta_T^2 over reduced range
            Y = integ.cumulative_trapezoid(gamma**2*beta_t[self.B_array_bg_subtracted_peaks[i][0][0]:self.B_array_bg_subtracted_peaks[i][0][-1]+1,0,i]**2,
                                           self.main_x_range[self.B_array_bg_subtracted_peaks[i][0][0]:self.B_array_bg_subtracted_peaks[i][0][-1]+1],
                                           initial = 0)
        
        #fit the resulting integrand
            fit = np.polyfit(X, Y, 1)
        #create the fit function
            linear_baseline = np.poly1d(fit) # create the linear baseline function
        
        #this subtracts the integrated K^2/2
            new_Y = Y-linear_baseline(X)
        #plt.plot(X[(self.B_peaks_x[0]-self.B_peaks_x[0][0])[0:-1]],new_Y[(self.B_peaks_x[0]-self.B_peaks_x[0][0])[0:-1]])
        
        #this again gives the positions of the poles. perhaps unnecessary
        #j_poles = X[(self.B_peaks_x[0]-self.B_peaks_x[0][0])[0:-1]]
        
        #phase error all the way through the device
            self.phase_error_array[i] = new_Y
        
        #phase error at each pole. plots what I would normally expect
            self.phase_error_array_j[:,0,i] = new_Y[(self.B_array_bg_subtracted_peaks[i][0]-self.B_array_bg_subtracted_peaks[i][0][0])[0:-1]]
        
        #determine local K from slope
            self.loc_K[0,i] = np.sqrt(2*linear_baseline[1])
        
        #these are the constants from the front of the equation
            phijconsts[0,i] = (2*np.pi/self.period_len_calc_array[i])/(1 + self.loc_K[0,i]**2/2)
        
        #take the mean of the collection
            local_phase_error_rad_array[0,i] = np.mean(phijconsts[0,i]*np.abs(self.phase_error_array_j[:,0,i]))
        
        #multiply up to degrees
            self.local_phase_error_deg_array[0,i] = local_phase_error_rad_array[0,i]*180/np.pi
        
        print('local phase error is {}'.format(self.local_phase_error_deg_array[0,i]))
        
        print('wait here')
        
        return self.local_phase_error_deg_array

    
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
            elif item == 'backgrBY_ar' or item == 'backgrBZ_ar' or item == 'B_peaks_x':
                pass
            
            elif item == 'I1' or item == 'I1_trap' or item == 'I1_trap_bg':
                print('{} is special and saved'.format(item))
                grp.require_dataset('{}'.format(item),  shape = self.__getattribute__(item).shape, dtype = self.__getattribute__(item).dtype)
                #this overwrites the existing dataset. It *should* be the same, but it's unsafe I guess
                #TODO fix this overwriting issue
                grp[item][...] = self.__getattribute__(item)
                grp[item].attrs['unit'] = 'Tmm'
                
            elif item == 'I2' or item == 'I2_trap'or item == 'I2_trap_bg':
                print('{} is special and saved'.format(item))
                grp.require_dataset('{}'.format(item),  shape = self.__getattribute__(item).shape, dtype = self.__getattribute__(item).dtype)
                #this overwrites the existing dataset. It *should* be the same, but it's unsafe I guess
                #TODO fix this overwriting issue
                grp[item][...] = self.__getattribute__(item)
                grp[item].attrs['unit'] = 'Tmm^2'
            
            elif item == 'trajectory':
                print('{} is special and saved'.format(item))
                grp.require_dataset('{}'.format(item),  shape = self.__getattribute__(item).shape, dtype = self.__getattribute__(item).dtype)
                #this overwrites the existing dataset. It *should* be the same, but it's unsafe I guess
                #TODO fix this overwriting issue
                grp[item][...] = self.__getattribute__(item)
                grp[item].attrs['unit'] = 'mm'
            
            elif item == 'B_array_bg_subtracted':
                print('{} is special and saved'.format(item))
                grp.require_dataset('{}'.format(item),  shape = self.__getattribute__(item).shape, dtype = self.__getattribute__(item).dtype)
                #this overwrites the existing dataset. It *should* be the same, but it's unsafe I guess
                #TODO fix this overwriting issue
                grp[item][...] = self.__getattribute__(item)
                grp[item].attrs['unit'] = 'T'
            elif item == 'main_x_range':
                print('{} is special and saved'.format(item))
                grp.require_dataset('{}'.format(item),  shape = self.__getattribute__(item).shape, dtype = self.__getattribute__(item).dtype)
                #this overwrites the existing dataset. It *should* be the same, but it's unsafe I guess
                #TODO fix this overwriting issue
                grp[item][...] = self.__getattribute__(item)
                grp[item].attrs['unit'] = 'mm'
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

    def find_central_axis(self):
        central_axis=np.zeros(len(self.B_peaks_x[0]))
        for i in range (len(self.B_peaks_x[0])):
            fine_z_array = np.linspace(-36,-26,1001)
            z_axis = np.linspace(self.z_start, self.z_end, 11)
            absoulute_array=abs(self.B_array_bg_subtracted[self.B_peaks_x[0][i],0,:,0])
            my_polyfit = np.polyfit(z_axis, absoulute_array,3)
            poly = np.poly1d(my_polyfit)
        #    poly(fine_z_array)
            central_value = fine_z_array[np.where(poly(fine_z_array)==np.min(poly(fine_z_array)))]
 
        central_axis_linefit = my_polyfit = np.polyfit(np.arange(len(central_axis)), central_axis,1)
        line_fit_fn = np.poly1d(central_axis_linefit)
        
        print('Pole 0 = {}'.format(line_fit_fn(0)))
        print('Pole 149 = {}'.format(line_fit_fn(149)))
        
        print('The central value here is {}'.format(central_value))
        return line_fit_fn
            
##area for custom exception
class IncompleteMetadataError(Exception):
    def __init__(self,message):
#        m = ''
#        for elem in missing_metadata:
#            m += elem + ', '
#        message = 'This measurement is missing the metadata for {}'.format(m[:-2])
        super().__init__(message)
        #can this error later highlight the missing boxes??