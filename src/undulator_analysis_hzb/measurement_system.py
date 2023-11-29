'''
Measurement_System
==================

Describes a Measurement System.

The Measurement System Module handles all classes to do
with the measurement systems - primarily the 
``Measurement_System`` class


Created on Oct 26, 2023

@author: oqb
'''
import numpy as np


class Measurement_System(object):
    """
    This is the Measurement_System Class
    
    The Measurement System Class describes a measurement system
    including all relevant motion control and sensor details.
    The class enables reading/writing to a main hdf5 datafile.
    
    Attributes
    ----------
    
    Optional Attributes
    -------------------
    
    """
    #TODO override equality operator
    def __init__(self,name,**kwargs):
        """
        Initialising a Measurement_System object.
        
        Parameters
        ----------
        name : str
            This is the common name of the measurement device.
        
        
        
        Optional Parameters
        -------------------
        x_calib_senis : numpy.ndarray
            a numpy array relating voltage to magnetic field in the x direction.
        y_calib_senis : numpy.ndarray
            a numpy array relating voltage to magnetic field in the y direction.
        z_calib_senis : numpy.ndarray
            a numpy array relating voltage to magnetic field in the z direction.
        
        
        Examples
        --------
        
        """
        self.name = name
        
        for key, value in kwargs.items():
            self.__setattr__(key, value)
            
        
    def load_hall_calibration_files(self,x_file, y_file, z_file):
        """
        This function loads hall calibration files for the granite measurement
        bench. It reads files and assigns the data within the files to 
        instance variables in the Measurement System Class
        
        Parameters
        ----------
        x_file : File()
            File or string object for location of x_calb_senis file.
        
        y_file : File()
            File or string object for location of y_calb_senis file.
            
        z_file : File()
            File or string object for location of z_calb_senis file.
        
        Attributes
        --------------
        x_calib_xenis : numpy.ndarray
            This numpy array holds the Voltage (V) - Field (B) characteristic curve for
            the X-orientation Hall Probe.
        y_calib_xenis : numpy.ndarray
            This numpy array holds the Voltage (V) - Field (B) characteristic curve for
            the X-orientation Hall Probe.
        z_calib_xenis : numpy.ndarray
            This numpy array holds the Voltage (V) - Field (B) characteristic curve for
            the X-orientation Hall Probe.
            
        
        """
        self.files = [x_file, y_file, z_file]
        self.x_calib_senis = np.genfromtxt(x_file)
        self.y_calib_senis = np.genfromtxt(y_file)
        self.z_calib_senis = np.genfromtxt(z_file)
        
    def save_measurement_system_group(self,grp):
        for item in self.__dict__:
            print(item)
            if item == 'files':
                #TODO save filenames
                pass
            elif isinstance(self.__getattribute__(item), np.ndarray):
                grp.create_dataset(item, data = self.__getattribute__(item))
                #TODO save attributes and axes etc
            
            else:
                print(item)
                grp.attrs[item] = self.__getattribute__(item)
                
            