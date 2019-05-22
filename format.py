# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:49:49 2019

@author: dell
"""

def format_RMC(s_file):
    
    s_file = s_file.upper()
    
    l_file = []
    l_file = list(s_file)
    
    l_file.append('\n')
    
    #删除所有的'\t'和'\r'
    length = len(l_file)
    j = 0
    while j < length:
        if l_file[j] == '\t' or l_file[j] == '\r':
            l_file[j] = ' '
        j  = j + 1
        
    #删除所有的注释
    length = len(l_file)
    j = 0
    while j < length:
        if l_file[j] == '/' and l_file[j+1] == '/':
            k = 0
            while l_file[j+2] != '\n':
                del l_file[j+2]
                k = k + 1   #记录被删除的注释字符数
            if j!= 0:
                x = j
                while l_file[x-1] ==' ':
                    x = x-1
                if l_file[x-1] == '\n':
                    del l_file[j:j+3]
                    length = length - k - 3
                else:
                    del l_file[j:j+2]
                    length = length - k - 2
                
                j = j - 1
            else:
                del l_file[j:j+3]
                length = length - k - 3
                j = j - 1
        j = j + 1
  
    #在等号和其他布尔符号两边加上空格
    length = len(l_file)
    j = 0
    while j < length:
        if (l_file[j] == '=' or 
            l_file[j] == ':' or 
            l_file[j] == '&' or 
            l_file[j] == '>' or
            l_file[j] == '(' or 
            l_file[j] == ')' or 
            l_file[j] == ',' or
            l_file[j] == '!'):
            l_file.insert(j + 1, ' ')
            l_file.insert(j, ' ')
            length = length + 2
            j = j + 1
        j = j + 1
        
    #删除空行中的空格&删除续行中的回车符
    length = len(l_file)
    j = 0
    while j < length - 1:
        
        if l_file[j] == '\n' and l_file[j + 1] == ' ':
            k = 1
            while l_file[j + k] == ' ':
                k = k + 1
            
            if l_file[j + k] == '\n':   #如果遇到了空行中有空格的情况：
                del l_file[j + 1:j + k]
                length = length - (k - 1)
            else:
                del l_file[j]       #如果遇到了是续行的情况：
                length = length - 1
                
        j = j + 1
    
    #删除行末的空格
    length = len(l_file)
    j = 0
    while j < length:
        while l_file[j] == '\n' and l_file[j - 1] == ' ':
            del l_file[j - 1]
            length =  length - 1
            j = j - 1
        j = j + 1
    
    #删除最开始的回车
    while l_file[0] == '\n':
        del l_file[0]
        
    #删除结尾的换行符
    index = len(l_file)
    while l_file[index-1] == '\n':
        del l_file[index-1]
        index = index - 1
    #l_file.append('\n')
    
    #删除连续的空格
    length = len(l_file)
    j = 0
    while j < length:
        while l_file[j] == ' ' and l_file[j + 1] == ' ':
            del l_file[j + 1]
            length = length - 1
        j = j + 1
        
    #删除三个及以上的换行符
    length = len(l_file)
    j = 0
    while j < length - 2:
        while l_file[j] == '\n' and l_file[j + 1] == '\n' and l_file[j + 2] == '\n':
            del l_file[j + 2]
            length = length - 1
        j = j + 1
        
    return ''.join(l_file)

    