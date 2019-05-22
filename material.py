# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:48:46 2019

@author: dell
"""

class material_r:
    def __init__(self):
        self.l_mat = []
        #未考虑MgAce和CeAce的部分
        
    def read_RMC(self, s_block):
        l_line = s_block.split('\n')
        j = 1
        length = len(l_line)
        while j < length:
            s_line = l_line[j]
            if s_line[0] == 'M':
                c_mat = mat_r()
            else:
                
                c_mat = sab_r()
            c_mat.readRMC(s_line)
            self.l_mat.append(c_mat)
            j = j + 1
            
            
class mat_r:
    def __init__(self):
        self.name = 'mat'
        self.id = 0
        self.density = 0
        self.zaid = []
        self.fraction = []
        
    def readRMC(self, s_line):
        l_value = s_line.split(' ')
        self.id = l_value[1]
        self.density = l_value[2]
        l_zaid_frac = l_value[3:]
        i = 0
        while i < len(l_zaid_frac):
            self.zaid.append(l_zaid_frac[i])
            i = i + 1
            self.fraction.append(l_zaid_frac[i])
            i = i + 1
            
        if str(self.density) == '0' or str(self.density) == '-0':  #如果密度为0，将各组分的份额直接相加作为密度
            self.density = 0
            for i in self.fraction:
                self.density = self.density + float(i)
            self.density = str(self.density)
        
        
class sab_r:
    def __init__(self):
        self.name = 'sab'
        self.id = 0
        self.zaid = ''
        
    def readRMC(self, s_line):
        l_value = s_line.split(' ')
        self.id = l_value[1]
        self.zaid = l_value[2]
        
class material_m:
    def __init__(self):
        self.l_mat = []
        
    def write_MCNP(self):
        s_out = ''
        for c_mat in self.l_mat:
            s_out = s_out + c_mat.write_MCNP()
        return s_out
    
class mat_m:
    def __init__(self):
        self.id = 0
        self.zaid = []
        self.fraction = []
        
    def write_MCNP(self):
        s = 'M'
        s = s + self.id + ' '
        for i in range(0, len(self.zaid)):
            s = s + self.zaid[i] + ' ' + self.fraction[i] + '\n'
            if i != len(self.zaid) - 1:
                s = s + '      '    #加上六个空格表示接着上一行
           
        return s
        
class mt_m:
    def __init__(self):
        self.id = 0
        self.zaid = ''
        
    def write_MCNP(self):
        s = ''
        s = s + 'MT' + self.id + ' '
        s = s + self.zaid + '\n'
        return s
    
def material_rmc_to_mcnp(c_r):
    c_m = material_m()
    for cf_r in c_r.l_mat:
        c_m.l_mat.append(mat_rmc_to_mcnp(cf_r))
        
    return c_m

def mat_rmc_to_mcnp(cf_r):
    if cf_r.name == 'mat':
        cf_m = mat_m()
        cf_m.id = cf_r.id
        cf_m.zaid = cf_r.zaid
        cf_m.fraction = cf_r.fraction
    elif cf_r.name == 'sab':
        cf_m = mt_m()
        cf_m.id = cf_r.id
        cf_m.zaid = cf_r.zaid
        
    return cf_m
    