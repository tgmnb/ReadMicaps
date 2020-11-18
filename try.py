# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 08:58:45 2020

@author: hp1020
"""

import sys
sys.path.append('D:\pyread')
import MiReadClass as mic

forder1='D:\\sd\\micaps\\t-td\\'
fordert='D:\\sd\\micaps\\t\\'
ofile='D:\Python\output\\'

v1='\\500\\'
file1='13052520.000'
vert=mic.Eqpt(file1,ofile,500,t=forder1+v1,td=fordert+v1)
vert.Culw()