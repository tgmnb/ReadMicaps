# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 11:48:09 2020

@author: hp1020
"""

import sys
sys.path.append('C:\\Users\\hp1020\\Documents\\GitHub\\ReadMicaps\\')
import MiReadClass as mic

forder1='D:\\sd\\micaps\\uv\\'
ofile='D:\Python\output\\'

v1='\\500\\'
file1='13052520.000'
vert=mic.Vert(file1,ofile,500,u=forder1+v1)
vert.Sped()
'''

file2='13052620.000'
vert=mic.Vert(file2,ofile,500,u=forder1+v1)
vert.Sped()

v2='\\850\\'
file1='13052520.000'
vert=mic.Vert(file1,ofile,850,u=forder1+v2)
vert.Sped()

file2='13052620.000'
vert=mic.Vert(file2,ofile,850,u=forder1+v2)
vert.Sped()

v3='\\1000\\'
file1='13052520.000'
vert=mic.Vert(file1,ofile,1000,u=forder1+v3)
vert.Sped()

file2='13052620.000'
vert=mic.Vert(file2,ofile,1000,u=forder1+v3)
vert.Sped()'''