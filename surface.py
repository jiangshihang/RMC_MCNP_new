# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:48:26 2019

@author: dell
"""

class surface_r:
    '''
    这是用于接收和输出RMC输入卡数据的类
    '''
    def __init__(self):
        self.l_surf = []
        
    def read_RMC(self, s_block):
        l_line = s_block.split('\n')
        j = 1
        length = len(l_line)
        while j < length:
            s_line = l_line[j]
            c_surf = surf_r()
            c_surf.readRMC(s_line)
            self.l_surf.append(c_surf)
            j = j + 1
    
class surf_r:
    def __init__(self):
        self.id = 0
        self.type = 'P'
        self.params = []
        self.bc = 0
        
    def readRMC(self, s_line):
        l_value = s_line.split(' ')
        self.id = l_value[1]
        self.type = l_value[2]
        if l_value.count('BC') != 0:
            k = l_value.index('BC')
            self.bc = l_value[k + 2]
            del l_value[k:]
        self.params = l_value[3:]
        

class surface_m:
    '''
    这是用于接收和输出MCNP输入卡数据的类
    '''
    def __init__(self):
        self.l_surf = []
        
    def write_MCNP(self):
        s_out = '\n'    #surface输入卡前面和universe卡之间要空一行
        for c_surf in self.l_surf:
            s_out = s_out + c_surf.write_MCNP()
        s_out = s_out + '\n'    #surface输入卡后面和data卡之间要空一行
        return s_out
            

class surf_m:
    def __init__(self):
        self.id = 0
        self.type = 'P'
        self.params = []
        self.bc = 0
        
    def write_MCNP(self):
        s = ''
        if self.bc == '1':
            s = s + '*'     #对于全反射面，在曲面编号前加*
        s = s + self.id + ' ' + self.type + ' ' + ' '.join(self.params) + '\n'
        #依次输出：曲面编号、类型、参数，换行符在最后输出
        return s

def surface_rmc_to_mcnp(c_r):
    '''
    这是用于从RMC类向MCNP类转换的函数
    '''
    c_m = surface_m()
    for cf_r in c_r.l_surf:
        c_m.l_surf.append(surf_rmc_to_mcnp(cf_r))
        
    return c_m
    
    
def surf_rmc_to_mcnp(cf_r):
    cf_m = surf_m()
    cf_m.bc = cf_r.bc
    cf_m.id = cf_r.id
    cf_m.type = cf_r.type
    cf_m.params = cf_r.params
    return cf_m
    
#def surface_mcnp_to_rmc(c_m):
    '''
    这是用于从MCNP类向RMC类转换的函数
    '''