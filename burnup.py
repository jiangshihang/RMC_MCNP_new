# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 10:36:48 2019

@author: dell
"""

class burnup_r:
    def __init__(self):
        self.burncell = 0
        self.timestep = []
        self.power = []
        self.substep = 0
        self.inherent = 0
        self.acelib = ''
        self.outputcell = 0
        
    def read_RMC(self, s_block):
        l_line = s_block.split('\n')
        s_line = l_line[1]
        l_value = s_line.split(' ')
        self.burncell = l_value[1]
        
        s_line = l_line[2]
        l_value = s_line.split(' ')
        self.timestep = l_value[1:]
        
        s_line = l_line[3]
        l_value = s_line.split(' ')
        self.power = l_value[1]
        
        s_line = l_line[4]
        l_value = s_line.split(' ')
        self.substep = l_value[1]
        
        s_line = l_line[5]
        l_value = s_line.split(' ')
        self.inherent = l_value[1]
        
        s_line = l_line[6]
        l_value = s_line.split(' ')
        self.acelib = l_value[1]
        
        s_line = l_line[7]
        l_value = s_line.split(' ')
        self.outputcell = l_value[1]
        

class burnup_m:
    def __init__(self):
        self.time = []
        self.pfrac = []
        self.power = 0
        self.mat = []
        self.omit = []
        self.afmin = []
        self.bopt = []
        self.matvol = []
        self.matmod = []
        self.swapb = []
        
    def write_MCNP(self):
        s_out = 0
        return s_out