'''
Created on Oct 26, 2023

@author: oqb
'''

class Device(object):
    '''
    This is the top level class for a device and its measurements.
    '''


    def __init__(self, device_name):
        '''
        Constructor
        '''
        self.name = device_name
        
        self.campaigns = {}
        
    def add_campaign(self, campaign):
        self.campaigns[campaign.name] = campaign

class Campaign(object):
    def __init__(self,campaign_name):
        self.name = campaign_name
        
        self.components = {}
        
    def add_component(self,component):
        self.components[component.name] = component 
        
class Component(object):
    def __init__(self,component_name):
        self.name = component_name
        
        self.steps = {}
        
    def add_step(self,step):
        self.steps[step.name] = step
        
class Step(object):
    def __init__(self, step_name):
        self.name = step_name 
        
        self.states = {}
        
    def add_state(self,state):
        self.states[state.name] = state
        
class State(object):
    def __init__(self,state_name):
        
        self.name = state_name
        
        self.measurements = {}
        
        
    def add_measurement(self,measurement):
        self.measurements[measurement.name] = measurement
        
class Measurement(object):
    def __init__(self,measurement_name):
        self.name = measurement_name
        
        self.tracks = {}
        
    def add_track(self,track):
        self.tracks[track.name] = track
        
    def assign_iteration(self):
        pass
        #if track in self.tracks
        