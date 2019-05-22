# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:48:02 2019

@author: dell
"""

import universe
import surface
import material
import criticality
import tally
import burnup

def read_RMC(s_file):
    l_blockstring = s_file.split('\n\n')
    l_blocklist_r = [getblocklists(s_block) for s_block in l_blockstring]
    return l_blocklist_r

def getblocklists(s_block):
    l_blockkey = ['',0]
    l_blockkey[0] = getblockname(s_block)
    l_blockkey[1] = getblockkey(l_blockkey[0], s_block)
    return l_blockkey

def getblockname(s_block):
    l_line = s_block.split('\n')
    l_value = l_line[0].split(' ')
    return l_value[0]
    
def getblockkey(s_name, s_block):
    if s_name == 'UNIVERSE':
        c_block = universe.universe_r()
        c_block.read_RMC(s_block)
    elif s_name == 'SURFACE':
        c_block = surface.surface_r()
        c_block.read_RMC(s_block)
    elif s_name == 'MATERIAL':
        c_block = material.material_r()
        c_block.read_RMC(s_block)
    elif s_name == 'CRITICALITY':
        c_block = criticality.criticality_r()
        c_block.read_RMC(s_block)
    elif s_name == 'TALLY':
        c_block = tally.tally_r()
        c_block.read_RMC(s_block)
    elif s_name == 'BURNUP':
        c_block = burnup.burnup_r()
        c_block.read_RMC()
    else:
        return 0
    
    return c_block

def change(l_block_r):
    #将读取得到的RMC输入卡类的列表转换成MCNP的输入卡类的列表
    l_block_m = []
    for l_blockkey_r in l_block_r:
        if l_blockkey_r[0] == 'UNIVERSE':
            l_blockkey_m = ['UNIVERSE',0]
            l_blockkey_m[1] = universe.univ_rmc_to_mcnp(l_blockkey_r[1],l_block_r)
            l_block_m.append(l_blockkey_m)
            
        elif l_blockkey_r[0] == 'SURFACE':
            l_blockkey_m = ['SURFACE',0]
            l_blockkey_m[1] = surface.surface_rmc_to_mcnp(l_blockkey_r[1])
            l_block_m.append(l_blockkey_m)
        elif l_blockkey_r[0] == 'MATERIAL':
            l_blockkey_m = ['MATERIAL',0]
            l_blockkey_m[1] = material.material_rmc_to_mcnp(l_blockkey_r[1])
            l_block_m.append(l_blockkey_m)
            
        elif l_blockkey_r[0] == 'TALLY':
            continue
        elif l_blockkey_r[0] == 'CRITICALITY':
            l_blockkey_m = ['CRITICALITY',0]
            l_blockkey_m[1] = criticality.criti_rmc_to_mcnp(l_blockkey_r[1])
            l_block_m.append(l_blockkey_m)
            
        elif l_blockkey_r[0] == 'BURNUP':
            continue
        
    return l_block_m
    

def write_MCNP(l_block):
    s_out = 'mcnp\n'
    for l_blockkey in l_block:
        if l_blockkey[1] != 0:
            s_out = s_out + l_blockkey[1].write_MCNP()
            
    return s_out
    