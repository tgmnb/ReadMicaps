# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:52:51 2020

@author: hp1020
"""

import sys
sys.path.append('C:\\Users\\hp1020\\Documents\\GitHub\\ReadMicaps\\')
import MiReadClass as mic

forder1='D:\\sd\\micaps\\uv\\'
fordert='D:\\sd\\micaps\\t\\'
ofile='D:\Python\output\\'

v1='\\500\\'
file1='13052520.000'
tadv=mic.Tadv(file1,ofile,500,u=forder1+v1,t=fordert+v1)
tadv.Adve()