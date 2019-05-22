# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 22:48:39 2019

@author: dell
"""
import surface
import math

class universe_r:
    def __init__(self):
        self.id = []
        self.move = []
        self.rotate = []
        self.lat = 0
        self.pitch = 0
        self.scope = 0
        self.sita = 0
        self.fill = 0
        self.l_cell = []
        
    def read_RMC(self, s_block):
        l_line = s_block.split('\n')
        
        s_line = l_line[0]
        l_value = s_line.split(' ')
        self.id = l_value[1]
        
        j = 1
        length = len(l_line)
        while j < length:
            s_line = l_line[j]
            c_cell = cell_r()
            c_cell.readRMC(s_line)
            self.l_cell.append(c_cell)
            j = j + 1
            
        s_line = l_line[0]
        l_value = s_line.split(' ')
        for i in range(len(l_value)):
            if l_value[i] == 'MOVE':
                self.move = l_value[i+2:i+5]
                continue
            if l_value[i] == 'ROTATE':
                self.rotate = l_value[i+2:i+11]
                continue
            if l_value[i] == 'LAT':
                self.lat = int(l_value[i+2])
                continue
            if l_value[i] == 'SCOPE' and self.lat == 1:
                self.scope = l_value[i+2:i+5]           
                continue
            if l_value[i] == 'SCOPE' and self.lat == 2:
                self.scope = l_value[i+2:i+4]
                continue
                
            if l_value[i] == 'PITCH' and self.lat == 1:
                self.pitch = l_value[i+2:i+5]
                continue
            if l_value[i] == 'PITCH' and self.lat == 2:
                self.pitch = l_value[i+2:i+4]
                continue
            
            if l_value[i] == 'SITA':
                self.sita = l_value[i+2]
                continue
                
            if l_value[i] == 'FILL':
                self.fill = l_value[i+2:]

            
class cell_r:
    def __init__(self):
        self.id = 0
        self.surf_bool = []
        self.mat = 0
        self.vol = 0
        self.tmp = 0
        self.void = 0
        self.fill = 0
        self.inner = 0
        self.move = []
        self.rotate = []
        
    def readRMC(self, s_line):
        l_value = s_line.split(' ')
        #读入栅元编号
        self.id = l_value[1]
        #读入栅元材料、体积、温度、追踪信息、填充空间、是否为内部栅元、平移和旋转的信息
        for i in range(len(l_value)):
            if l_value[i] == 'MAT':
                self.mat = l_value[i + 2]
            if l_value[i] == 'VOL':
                self.vol = l_value[i + 2]
            if l_value[i] == 'TMP':
                self.tmp = l_value[i + 2]
            if l_value[i] == 'VOID':
                self.void = l_value[i + 2]
            if l_value[i] == 'INNER':
                self.inner = l_value[i + 2]
            if l_value[i] == 'MOVE':
                self.move = l_value[i+2:i+5]
            if l_value[i] == 'ROTATE':
                self.rotate = l_value[i+2:i+11]
            if l_value[i] == 'FILL':
                self.fill = l_value[i + 2]
                
        #读入栅元的曲面布尔定义
        i = 2
        while (i < len(l_value) and
               l_value[i] != 'MAT' and
               l_value[i] != 'VOL' and
               l_value[i] != 'TMP' and
               l_value[i] != 'VOID' and
               l_value[i] != 'INNER' and
               l_value[i] != 'MOVE' and
               l_value[i] != 'ROTATE' and
               l_value[i] != 'FILL'):
            
            self.surf_bool.append(l_value[i])
            i = i + 1
            
class universe_m:
    def __init__(self):
        self.cells = []
        
    def write_MCNP(self):
        s_out = ''
        for c_cell in self.cells:
            s = c_cell.write_MCNP()
            s_out = s_out + s
        
        return s_out
    
    
class cell_m:
    def __init__(self):
        self.id = 0
        self.matid = 0
        self.density = 0
        self.surf_bool = []
        self.imp = 1
        self.vol = 0
        self.u = 0
        self.trcl = []
        self.lat = 0
        self.fill = []  #注意：MCNP在重复结构里，fill包含了前面的pitch和具体填充的栅元
        self.tmp = 0
        
    def write_MCNP(self):
        s = ''
        s = s + self.id + ' '
        if str(self.matid) != '0':
            s = s + str(self.matid) + ' ' + str(self.density) + ' '
        else:
            s = s + str(self.matid) + ' '
        
        s = s + ' '.join(self.surf_bool) + ' '  #输出栅元的曲面布尔定义
        if str(self.tmp) != '0':
            s = s + 'TMP=' + self.tmp + ' '
        
        if self.u != 0:
            s = s + 'U=' + self.u + ' '
        if self.trcl != []:
            s = s + 'TRCL=(' + ' '.join(self.trcl) + ') '
        s = s + 'IMP:N=' + str(self.imp) + ' '
        
        leng = len(s)       #得到此时字符串的长度
        j = int(leng/80)   #判断是否超过了80列，如果是的话，插入换行标志
        if j != 0:
            i = 79
            leng1 = leng

            l = list(s)
            while leng1 > 79:
                
                while l[i] != ' ':
                    i = i - 1
                l.insert(i, '&\n')
                leng1 = leng - i
                i = i + 79
                
            leng2 = len(l)
            if l[leng2-1] == ' ':
                del l[leng2-1]
                if l[leng2-2] == '&\n':
                    del l[leng2-2]
            s = ''.join(l)
        
        if str(self.lat) != '0':       #如果是重复序列填充
            s = s + '&\n'
            s = s + 'LAT=' + str(self.lat) + ' '
            s = s + 'FILL='
            scope_x = float(self.fill[2]) - float(self.fill[0]) + 1
            scope_x = int(scope_x)
            if str(self.lat) == '1':
                s = s + ' '.join(self.fill[0:9]) + '\n      '
                r1 = 0
                for s1 in self.fill:
                    if s1.count('r') != 0:
                        r1 = 1
                if r1 == 1:
                    s = s + ' '.join(self.fill[9:])
                
                else:
                    k = 1
                    while 8 + k*scope_x <= len(self.fill):
                        s = s + ' '.join(self.fill[9+(k-1)*scope_x : 9 + k*scope_x])
                        k = k + 1
                        if 8 + k*scope_x <= len(self.fill):
                            s = s + '\n      '
                s = s + '\n'
            if str(self.lat) == '2':
                s = s + ' '.join(self.fill[0:9]) + '\n      '
                r2 = 0
                for s2 in self.fill:
                    if s2.count('r') != 0:
                        r2 = 1
                if r2 == 1:
                    s = s + ' '.join(self.fill[9:])
                
                else:
                    k = 1
                    while 8 + k*scope_x <= len(self.fill):
                        s = s + ' '.join(self.fill[9+(k-1)*scope_x : 9 + k*scope_x])
                        k = k + 1
                        if 8 + k*scope_x <= len(self.fill):
                            s = s + '\n      '
                s = s + '\n'

        elif self.fill != [] and self.fill != 0 and self.fill != '0':
            s = s + 'FILL= ' + str(self.fill)
            s = s + '\n'
        else:
            s = s + '\n'
        return s
        
def univ_rmc_to_mcnp(c_r, l_block_r):
    c_m = universe_m()
    for cf_r in c_r.l_cell:
        c_m.cells.append(cell_rmc_to_mcnp(cf_r, c_r, l_block_r))
        
    if c_r.l_cell == []:
        c_m.cells.append(cell_rmc_to_mcnp2(c_r, l_block_r))
    return c_m

def cell_rmc_to_mcnp(cf_r, c_r ,l_block_r):
    #这是对于一般的填充栅元
    cf_m = cell_m()
    cf_m.id = cf_r.id
    cf_m.vol = cf_r.vol
    cf_m.matid = cf_r.mat
    cf_m.surf_bool = change_surf_bool_RM(cf_r.surf_bool)
    cf_m.u = c_r.id
    cf_m.fill = cf_r.fill

    if cf_r.tmp != 0:
        cf_m.tmp = str(float(cf_r.tmp)*8.617e-11)   #温度的转换
    
    #确定对栅元进行的空间变换TRCL
    if str(cf_r.void) == '0':
        cf_m.imp = '1'
    else:
        cf_m.imp = '0'
    if cf_m.matid != '0':
        cf_m.density = find_density(l_block_r, cf_r.mat)
        
        cf_m.trcl = []
    if c_r.move != []:
        cf_m.trcl = c_r.move
    else:
        cf_m.trcl = ['0','0','0']
    if c_r.rotate != []:
        cf_m.trcl = cf_m.trcl + c_r.rotate
    else:
        cf_m.trcl = cf_m.trcl + ['1','0','0','0','1','0','0','0','1']
    if cf_m.trcl == ['0','0','0','1','0','0','0','1','0','0','0','1']:
        cf_m.trcl = []
        
    return cf_m
    
def cell_rmc_to_mcnp2(c_r, l_block_r):
    #这是对于包含重复结构的栅元
    cf_m = cell_m()
    cf_m.matid = '0'
    #cf_m.density = '1'
    cf_m.id = str(int(c_r.id)+200)
    cf_m.lat = c_r.lat
    cf_m.fill = []
    sita = float(c_r.sita)/180*math.pi
    if str(cf_m.lat) == '1':
        #对于长方体填充的情况
        cf_m.fill = cf_m.fill + ['0',':',str(int(c_r.scope[0])-1)]
        cf_m.fill = cf_m.fill + ['0',':',str(int(c_r.scope[1])-1)]
        cf_m.fill = cf_m.fill + ['0',':',str(int(c_r.scope[2])-1)]
        l_fill_cell = c_r.fill
        s_fill_cell = ' '.join(l_fill_cell)
        if s_fill_cell.count('*') != 0:     #如果是*格式的重复填充
            l_fill_cell = []
            l_divide = s_fill_cell.split(' ')   #分别对每个cell重复填充处理
            for s_fill_cell0 in l_divide:
                l_cell_repeat = s_fill_cell0.split('*')  #以*号为分割，则得到的列表第一项为cell编号，第二项为重复填充次数
                l_fill_cell.append(l_cell_repeat[0])
                i_times = int(l_cell_repeat[1])
                l_fill_cell.append(str(i_times - 1) + 'r')

        cf_m.fill = cf_m.fill + l_fill_cell
        
        #因为RMC和MCNP在立方重复结构填充的时候，选取的原点不同
        #RMC选取的是立方的一个角作为原点，MCNP选取的是立方的中心
        #因此，需要在填充后做一个初始平移使二者处在相同的位置上
        #cf_m.trcl = [str(float(c_r.pitch[0])/2),str(float(c_r.pitch[1])/2),str(float(c_r.pitch[2])/2)]
        #cf_m.trcl = cf_m.trcl + ['1','0','0','0','1','0','0','0','1']
        
    elif str(cf_m.lat) == '2':
        #对于六边形填充的情况:
        cf_m.fill = cf_m.fill + ['0',':',str(int(c_r.scope[0])-1)]
        cf_m.fill = cf_m.fill + ['0',':',str(int(c_r.scope[1])-1)]
        
        '''
        if int(c_r.scope[0])%2 != 0:   #如果某一边上的scope是奇数
            cf_m.fill = cf_m.fill + [str(-(int(c_r.scope[0])-1)/2),':',str((int(c_r.scope[0])-1)/2)]
        else:                           #如果scope是偶数
            cf_m.fill = cf_m.fill + [str(-(int(c_r.scope[0]))/2+1),':',str((int(c_r.scope[0]))/2)]
            cf_m.trcl.append(str(-float(c_r.pitch[0])/2))
            cf_m.trcl = cf_m.trcl + ['0','0','1','0','0','0','1','0','0','0','1']
            
        if int(c_r.scope[1])%2 != 0:
            cf_m.fill = cf_m.fill + [str(-(int(c_r.scope[1])-1)/2),':',str((int(c_r.scope[1])-1)/2)]
        else:
            cf_m.fill = cf_m.fill + [str(-(int(c_r.scope[1]))/2+1),':',str((int(c_r.scope[0]))/2)]
            cf_m.trcl.append(str(-float(c_r.pitch[1])*math.cos(sita)/2))
            cf_m.trcl.append(str(-float(c_r.pitch[1])*math.sin(sita)/2))
            cf_m.trcl = cf_m.trcl + ['0','1','0','0','0','1','0','0','0','1']
        '''
        cf_m.fill = cf_m.fill + ['0',':','0']
        l_fill_cell = c_r.fill
        s_fill_cell = ''.join(l_fill_cell)
        if s_fill_cell.count('*') != 0:     #如果是*格式的重复填充
            l_fill_cell = []
            l_divide = s_fill_cell.split(' ')   #分别对每个cell重复填充处理
            for s_fill_cell0 in l_divide:
                l_cell_repeat = s_fill_cell.split('*')  #以*号为分割，则得到的列表第一项为cell编号，第二项为重复填充次数
                l_fill_cell.append(l_cell_repeat[0])
                i_times = int(l_cell_repeat[1])
                l_fill_cell.append(str(i_times - 1) + 'r')

        cf_m.fill = cf_m.fill + l_fill_cell
    
    if c_r.move != []:
        if cf_m.trcl != []:
            cf_m.trcl[0] = str(float(cf_m.trcl[0]) + float(c_r.move[0]))
            cf_m.trcl[1] = str(float(cf_m.trcl[1]) + float(c_r.move[1]))
            cf_m.trcl[2] = str(float(cf_m.trcl[2]) + float(c_r.move[2]))
        else:
            cf_m.trcl = c_r.move
            cf_m.trcl = cf_m.trcl + ['1','0','0','0','1','0','0','0','1']
    
    if c_r.rotate != []:
        if cf_m.trcl != []:
            cf_m.trcl[3:12] = c_r.rotate
        
        else:
            cf_m.trcl = ['0','0','0']
            cf_m.trcl = cf_m.trcl + c_r.rotate
            
    
    #确定对栅元进行的空间变换TRCL
    '''
    cf_m.trcl = []
    if c_r.move != []:
        cf_m.trcl = c_r.move
    else:
        cf_m.trcl = ['0','0','0']
    if c_r.rotate != []:
        cf_m.trcl = cf_m.trcl + c_r.rotate
    else:
        cf_m.trcl = cf_m.trcl + ['0','0','0','0','0','0','0','0','0']
    if cf_m.trcl == ['0','0','0','0','0','0','0','0','0','0','0','0']:
        cf_m.trcl = []
    '''
    cf_m.u = c_r.id
    
    #接下来要确定作为基准的重复结构的曲面布尔定义，为和RMC保持一致，取在原点
    if str(cf_m.lat) == '1':
        b1 = float(c_r.pitch[0])
        b2 = float(c_r.pitch[1])
        b3 = float(c_r.pitch[2])
        
        c_surf1 = surface.surf_r()
        c_surf2 = surface.surf_r()
        c_surf3 = surface.surf_r()
        c_surf4 = surface.surf_r()
        
        if str(c_r.scope[2]) != '0':    #一般不考虑三维的重复填充，如果需要的话再加上
            c_surf5 = surface.surf_r()
            c_surf6 = surface.surf_r()
            
        for l_blockkey in l_block_r:
            if l_blockkey[0] == 'SURFACE':
                c_surface = l_blockkey[1]
                
        l_surf = c_surface.l_surf
        length = len(l_surf)
        surf_id = int(l_surf[length - 1].id)
        c_surf1.id = str(surf_id + 1)
        c_surf2.id = str(surf_id + 2)
        c_surf3.id = str(surf_id + 3)
        c_surf4.id = str(surf_id + 4)
        
        c_surf1.type = 'PX'
        c_surf2.type = 'PX'
        c_surf3.type = 'PY'
        c_surf4.type = 'PY'
        
        c_surf1.params = [str(b1)]
        c_surf2.params = ['0']
        c_surf3.params = [str(b2)]
        c_surf4.params = ['0']
        
        bool1 = 0
        bool2 = 0
        bool3 = 0
        bool4 = 0

        for c_surf in l_surf:
            if c_surf.params == c_surf1.params and c_surf.type == c_surf1.type:
                c_surf1.id = c_surf.id
                bool1 = 1
            elif c_surf.params == c_surf2.params and c_surf.type == c_surf2.type:
                c_surf2.id = c_surf.id
                bool2 = 1
            elif c_surf.params == c_surf3.params and c_surf.type == c_surf3.type:
                c_surf3.id = c_surf.id
                bool3 = 1
            elif c_surf.params == c_surf4.params and c_surf.type == c_surf4.type:
                c_surf4.id = c_surf.id
                bool4 = 1
        
        if bool1 == 0:
            c_surface.l_surf.append(c_surf1)
        if bool2 == 0:
            c_surface.l_surf.append(c_surf2)
        if bool3 == 0:
            c_surface.l_surf.append(c_surf3)
        if bool4 == 0:
            c_surface.l_surf.append(c_surf4)
        
        cf_m.surf_bool = ['-'+str(c_surf1.id), str(c_surf2.id), '-'+str(c_surf3.id), str(c_surf4.id)]

    
    if str(cf_m.lat) == '2':    #如果是六边形重复结构
        b1 = float(c_r.pitch[0])
        b2 = float(c_r.pitch[1])
        sita = float(c_r.sita)/180*math.pi

        #计算六个曲面的参数
        c_surf1 = surface.surf_r()
        c_surf2 = surface.surf_r()
        c_surf3 = surface.surf_r()
        c_surf4 = surface.surf_r()
        c_surf5 = surface.surf_r()
        c_surf6 = surface.surf_r()
        
        for l_blockkey in l_block_r:
            if l_blockkey[0] == 'SURFACE':
                c_surface = l_blockkey[1]   #从总列表中把surface类提取出来
                
        l_surf = c_surface.l_surf
        length = len(l_surf)
        surf_id = int(l_surf[length - 1].id)
        c_surf1.id = str(surf_id + 1)
        c_surf2.id = str(surf_id + 2)
        c_surf3.id = str(surf_id + 3)
        c_surf4.id = str(surf_id + 4)
        c_surf5.id = str(surf_id + 5)
        c_surf6.id = str(surf_id + 6)
        
        c_surf1.type = 'P'
        c_surf2.type = 'P'
        c_surf3.type = 'P'
        c_surf4.type = 'P'
        c_surf5.type = 'P'
        c_surf6.type = 'P'

        c_surf1.params = ['2','0','0',str(b1)]
        c_surf2.params = ['2','0','0',str(-b1)]
        c_surf3.params = [str(1/math.tan(sita)),'1','0',str(0.5*math.sqrt(b2*b2-b1*b1/4)+b1/(4*math.tan(sita)))]
        c_surf4.params = [str(1/math.tan(sita)),'1','0',str(-0.5*math.sqrt(b2*b2-b1*b1/4)-b1/(4*math.tan(sita)))]
        c_surf5.params = [str(-1/math.tan(sita)),'1','0',str(0.5*math.sqrt(b2*b2-b1*b1/4)+b1/(4*math.tan(sita)))]
        c_surf6.params = [str(-1/math.tan(sita)),'1','0',str(-0.5*math.sqrt(b2*b2-b1*b1/4)-b1/(4*math.tan(sita)))]
    
        bool1 = 0
        bool2 = 0
        bool3 = 0
        bool4 = 0
        bool5 = 0
        bool6 = 0
        for c_surf in l_surf:
            if c_surf.params == c_surf1.params and c_surf.type == c_surf1.type:
                c_surf1.id = c_surf.id
                bool1 = 1
            elif c_surf.params == c_surf2.params and c_surf.type == c_surf2.type:
                c_surf2.id = c_surf.id
                bool2 = 1
            elif c_surf.params == c_surf3.params and c_surf.type == c_surf3.type:
                c_surf3.id = c_surf.id
                bool3 = 1
            elif c_surf.params == c_surf4.params and c_surf.type == c_surf4.type:
                c_surf4.id = c_surf.id
                bool4 = 1
            elif c_surf.params == c_surf5.params and c_surf.type == c_surf5.type:
                c_surf5.id = c_surf.id
                bool5 = 1
            elif c_surf.params == c_surf6.params and c_surf.type == c_surf6.type:
                c_surf6.id = c_surf.id
                bool6 = 1
        
        if bool1 == 0:
            c_surface.l_surf.append(c_surf1)
        if bool2 == 0:
            c_surface.l_surf.append(c_surf2)
        if bool3 == 0:
            c_surface.l_surf.append(c_surf3)
        if bool4 == 0:
            c_surface.l_surf.append(c_surf4)
        if bool5 == 0:
            c_surface.l_surf.append(c_surf5)
        if bool6 == 0:
            c_surface.l_surf.append(c_surf6)
        
        cf_m.surf_bool = ['-'+str(c_surf1.id), str(c_surf2.id), '-'+str(c_surf3.id), str(c_surf4.id), '-'+str(c_surf5.id), str(c_surf6.id)]
        
    return cf_m


#用于转换曲面布尔定义的函数
def change_surf_bool_RM(l_bool_0):
    l_bool_1 = []
    i = 0
    while i < len(l_bool_0):
        if l_bool_0[i] != '(' and l_bool_0[i] != ')':
            l_bool_1.append(l_bool_0[i])
        else:
            if l_bool_0[i] == '(':
                j = i
                k = 1
                while(k!=0):
                    j = j + 1
                    if l_bool_0[j] == '(':
                        k = k + 1;
                    if l_bool_0[j] == ')':
                        k = k - 1;
                        #while循环结束后，j应表示之前的'('对应的')'
                l_bool_new = l_bool_0[i+1:j]
                l_bool_new = change_surf_bool_RM(l_bool_new) #递归
                l_bool_new.insert(0,'(')
                l_bool_new.append(')')
                s_bool_new = ''.join(l_bool_new)
                l_bool_1.append(s_bool_new)
                i = j
        i = i + 1
    #将括号内的内容作为一个整体，下面将针对&和：插入括号
    m = 0
    count = 0
    len2 = (len(l_bool_1))
    while(m<len2-1):
        if l_bool_1[m] == ':' or l_bool_1[m] == '&':
            if l_bool_1[m] == ':':
                n = m
                p = 0
                count=count+1
                if count == 1:
                    #找到第一个:前需要插入左括号的地方
                    m0 = m - 1
                    while l_bool_1 != ' ' and m0 > 0:
                        m0 = m0 - 1
                while l_bool_1[n] != '&':
                    #找到需要插入右括号的位置，找不到则p=1
                    n = n + 1
                    if n > len(l_bool_1)-1:
                        p = 1
                        break
                if p == 0:
                    l_bool_1.insert(n,')')
                    l_bool_1.insert(m0,'(')
                    len2 = len2 + 2
                    m = m + 1
        m = m + 1
    for i in range(len(l_bool_1)):
            if l_bool_1[i] == '&':
                l_bool_1[i] = ' '
            elif l_bool_1[i] == '!':
                l_bool_1[i] = '#'
                
    #删除多余的空格
    '''
    length = len(l_bool_1)
    j = 0
    while j < length:
        while l_bool_1[j] == ' ':
            del l_bool_1[j]
            length = length - 1
            j = j - 1
            
        j = j + 1
    '''
    return l_bool_1

#查找MCNP输入卡对应的cell的材料密度
def find_density(l_block, matid):
    for l_blockkey in l_block:
        if l_blockkey[0] == 'MATERIAL':
            c_material = l_blockkey[1]
            for c_mat in c_material.l_mat:
                if c_mat.id == matid:
                    return c_mat.density