# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:18:28 2019

@author: dell
"""

import rmc_to_mcnp
#import mcnp_to_rmc
import format

#正常输入模式

print("欢迎使用RMC-MCNP输入卡互转程序")
print("1：RMC转MCNP,2：MCNP转RMC")
str = input("请输入转换模式：")
name = input("请输入待转换文件名：")
name2 = input("请输入生成的文件名：")

if str == "1":
    s2 = format.format_RMC(open(name, 'r',encoding='UTF-8').read())
    #print(s2)
    l1 = rmc_to_mcnp.read_RMC(s2)
    l2 = rmc_to_mcnp.change(l1)
    ss2 = rmc_to_mcnp.write_MCNP(l2)
    f_ss2 = open(name2, 'w')
    f_ss2.write(ss2)
    f_ss2.close()
    
    
if str == "2":
    s1 = format.format_MCNP(open(name, 'r',encoding='UTF-8').read())
    l2 = mcnp_to_rmc.read_MCNP(s1)
    l2 = mcnp_to_rmc.change_list2(l2)
    ss1 = mcnp_to_rmc.write_RMC(l2)
    f_ss1 = open(name2, 'w')
    f_ss1.write(ss1)
    f_ss1.close()

#调试模式，在调试时可节省键入文字的时间
'''

s2 = format.format_RMC(open('inp_vera_assemly.txt', 'r').read())
#s2 = format.format_RMC(s2)
l1 = RM.read_RMC(s2)
l1 = RM.change_list(l1)
ss2 = RM.write_MCNP(l1)
f_ss2 = open('vera_MCNP', 'w')
f_ss2.write(ss2)
f_ss2.close()

s2 = format.format_MCNP(open('CASE_2', 'r').read())
#s2 = format.format_RMC(s2)
print(s2)
l1 = MR.read_MCNP(s2)
l1 = MR.change_list2(l1)
ss2 = MR.write_RMC(l1)
f_ss2 = open('CASE2_RMC', 'w')
f_ss2.write(ss2)
f_ss2.close()
'''