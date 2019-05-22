# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:49:29 2019

@author: dell
"""

class tally_r:
    def __init__(self):
        self.l_tallies = []
        self.map = 1
        self.union = 0
        
    def read_RMC(self, s_block):
        l_line = s_block.split('\n')
        i = 1
        num = len(l_line)
        while i < num:
            s_line = l_line[i]
            l_value = s_line.split(' ')
            if l_value[0] == 'CELLTALLY':
                c_tally = celltally_r()
                c_tally.readRMC(l_value)
                self.l_tallies.append(c_tally)
            if l_value[0] == 'MESHTALLY':
                c_tally = meshtally_r()
                c_tally.readRMC(l_value)
                self.l_tallies.append(c_tally)
            if l_value[0] == 'CSTALLY':
                c_tally = cstally_r()
                c_tally.readRMC(l_value)
                self.l_tallies.append(c_tally)
            else:
                j = 1
                length = len(l_value)
                while j < length:
                    if l_value[j] == 'MAP':
                        self.map = l_value[j+2]
                    if l_value[j] == 'UNION':
                        self.union = l_value[j+2]
                    j = j + 1
            i = i + 1
            
class celltally_r:
    def __init__(self):
        self.id = 0
        self.type = 1
        self.energy = []
        self.filter = []
        self.integral = []
        self.cell = []
        
    def readRMC(self, l_value):
        self.id = l_value[1]
        j = 2
        length = len(l_value)
        while j < length:
            if l_value[j] == 'TYPE':
                self.type = l_value[j+2]
            if l_value[j] == 'ENERGY':
                j = j + 2
                while (l_value[j] != 'FILTER' and
                       l_value[j] != 'INTEGRAL' and
                       l_value[j] != 'CELL'):
                    self.energy.append(l_value[j])
                    j = j + 1
                continue
                
            if l_value[j] == 'FILTER':
                j = j + 2
                while (l_value[j] != 'INTEGRAL' and
                       l_value[j] != 'CELL'):
                    self.filter.append(l_value[j])
                    j = j + 1
                continue
                
            if l_value[j] == 'INTEGRAL':
                j = j + 2
                while (l_value[j] != 'FILTER' and
                       l_value[j] != 'CELL'):
                    self.integral.append(l_value[j])
                    j = j + 1
                continue
            
            if l_value[j] == 'CELL':
                self.cell = l_value[j+2:]
            
            j = j + 1
            

class meshtally_r:
    def __init__(self):
        self.id = 0
        self.type = 1
        self.energy = []
        self.scope = []
        self.bound = []
        
    def readRMC(self, l_value):
        self.id = l_value[1]
        j = 2
        length = len(l_value)
        while j < length:
            if l_value[j] == 'TYPE':
                self.type = l_value[j+2]
            if l_value[j] == 'ENERGY':
                j = j + 2
                while(l_value[j] != 'SCOPE' and
                      l_value[j] != 'BOUND'):
                    self.energy.append(l_value[j])
                    j = j + 1
                continue
                
            if l_value[j] == 'SCOPE':
                self.scope = l_value[j+2,j+5]
                
            if l_value[j] == 'BOUND':
                self.bound = l_value[j+2,j+5]
                
            j = j + 1
            

class cstally_r:
    def __init__(self):
        self.id = 0
        self.cell = []
        self.mat = 0
        self.energy = []
        self.mt = []
        
    def readRMC(self, l_value):
        self.id = l_value[1]
        j = 2
        length = len(l_value)
        while j < length:
            if l_value[j] == 'CELL':
                j = j + 2
                while(l_value[j] != 'MAT' and
                      l_value[j] != 'ENERGY' and
                      l_value[j] != 'MT'):
                    self.cell.append(l_value[j])
                    j = j + 1
                continue
            
            if l_value[j] == 'MAT':
                self.mat = l_value[j+2]
                
            if l_value[j] == 'ENERGY':
                while(j < length and
                      l_value[j] != 'MT'):
                    self.energy.append(l_value[j])
                    j = j + 1
                continue
            
            if l_value[j] == 'MT':
                self.mt = l_value[j+2:]
                
'''
class tally_m:
    def __init__(self):
        
    def write_MCNP(self):
   '''     