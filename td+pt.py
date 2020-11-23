# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 12:35:04 2020
12354
@author: tgm
"""
import sys
sys.path.append('C:\\Users\\hp1020\\Documents\\GitHub\\ReadMicaps\\')
import MiReadClass as mic

#数据文件夹
forder1='D:\\sd\\micaps\\t-td\\'
fordert='D:\\sd\\micaps\\t\\'
ofile='D:\Python\output\\'
#数据
td1='\\500\\'
file1='13052520.000'
#输出文件夹
ldc=mic.MiR4(forder1+td1,file1,ofile,'t-td')
ldc.OutPutContour()

file2='13052620.000'
ldc=mic.MiR4(forder1+td1,file2,ofile,'t-td')
ldc.OutPutContour()


td2='\\850\\'
file1='13052520.000'
ldc=mic.MiR4(forder1+td2,file1,ofile,'t-td')
ldc.OutPutContour()

file2='13052620.000'
ldc=mic.MiR4(forder1+td2,file2,ofile,'t-td')
ldc.OutPutContour()

t1='\\500\\'
file1='13052520.000'
pt=mic.MiR4(fordert+t1,file1,ofile,'pt 500')
pt.OutPutContour()

file2='13052620.000'
pt=mic.MiR4(fordert+t1,file2,ofile,'pt 500')
pt.OutPutContour()

t2='\\850\\'
file1='13052520.000'
pt=mic.MiR4(fordert+t2,file1,ofile,'pt 850')
pt.OutPutContour()

file2='13052620.000'
pt=mic.MiR4(fordert+t2,file2,ofile,'pt 850')
pt.OutPutContour()




