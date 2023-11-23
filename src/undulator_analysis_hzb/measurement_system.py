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
            class attributes
            
            Parameters
            ----------
            x_file : File()
                File or string object for location of x_calb_senis file.
            
            y_file : File()
                File or string object for location of y_calb_senis file.
                
            z_file : File()
                File or string object for location of z_calb_senis file.
            
            New Attributes
            --------------
            
            
            """
            self.files = [x_file, y_file, z_file]
            self.x_calib_senis = np.genfromtxt(x_file)
            self.y_calib_senis = np.genfromtxt(y_file)
            self.z_calib_senis = np.genfromtxt(z_file)