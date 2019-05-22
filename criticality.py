# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:48:54 2019

@author: dell
"""

class criticality_r:
    def __init__(self):
        self.population = [0,0,0]
        self.keff = 1.0
        self.batch = 0
        self.src_type = ''
        self.params = []
        self.rng_type = 1
        self.seed = 1
        self.stride = 10000
        self.parallel = 0
        
    def read_RMC(self, s_block):
        l_line = s_block.split('\n')
        num = len(l_line)
        
        s_line = l_line[1]
        l_value = s_line.split(' ')
        j = 1
        length = len(l_value)
        while j < length:
            if l_value[j] == 'POPULATION':
                self.population = l_value[j+2:j+5]
            if l_value[j] == 'KEFF0':
                self.keff = l_value[j+2]
            if l_value[j] == 'BATCH':
                self.batch = l_value[j+2]
            j = j + 1
        
        if self.batch == 0:
            self.batch = int(self.population[2]) - int(self.population[1])
            
        s_line = l_line[2]
        l_value = s_line.split(' ')
        self.src_type = l_value[1]
        self.params = l_value[3:]
        
        if num > 3:
            s_line = l_line[3]
            if s_line[0] == 'R':
                l_value = s_line.split(' ')
                j = 1
                length = len(l_value)
                while j < length:
                    if l_value[j] == 'TYPE':
                        self.rng_type = l_value[j+2]
                    if l_value[j] == 'SEED':
                        self.seed = l_value[j+2]
                    if l_value[j] == 'STRIDE':
                        self.stride = l_value[j+2]
                        
            else:
                l_value = s_line.split(' ')
                self.parallel = l_value[1]
                
        if num > 4:
            s_line = l_line[4]
            l_value = s_line.split(' ')
            self.parallel = l_value[1]
            

class criticality_m:
    def __init__(self):
        self.kcode = []
        self.type = ''
        self.ksrc = []
        
    def write_MCNP(self):
        s_out = ''
        s_out = s_out + 'KCODE ' + ' '.join(self.kcode) + '\n'
        s_out = s_out + 'KSRC ' + ' '.join(self.ksrc) + '\n'
        return s_out
    
def criti_rmc_to_mcnp(c_r):
    c_m = criticality_m()
    c_m.kcode = []
    c_m.kcode.append(str(c_r.population[0]))
    c_m.kcode.append(str(c_r.keff))
    c_m.kcode.append(str(c_r.population[1]))
    c_m.kcode.append(str(c_r.population[2]))
    c_m.ksrc = c_r.params
    
    return c_m