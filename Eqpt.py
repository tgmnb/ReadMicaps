# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 08:58:45 2020

@author: hp1020
"""

import sys
sys.path.append('C:\\Users\\hp1020\\Documents\\GitHub\\ReadMicaps\\')
import MiReadClass as mic

forder1='D:\\sd\\micaps\\t-td\\'
fordert='D:\\sd\\micaps\\t\\'
ofile='D:\Python\output\\'

v1='\\500\\'
file1='13052520.000'
eqpt=mic.Eqpt(file1,ofile,500,t=forder1+v1,td=fordert+v1)
eqpt.Culw()

file2='13052620.000'
eqpt=mic.Eqpt(file2,ofile,500,t=forder1+v1,td=fordert+v1)
eqpt.Culw()

v2='\\850\\'
file1='13052520.000'
eqpt=mic.Eqpt(file1,ofile,500,t=forder1+v2,td=fordert+v2)
eqpt.Culw()

file2='13052620.000'
eqpt=mic.Eqpt(file2,ofile,500,t=forder1+v2,td=fordert+v2)
eqpt.Culw()
