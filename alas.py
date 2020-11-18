# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 12:35:04 2020

@author: tgm
"""
import sys
sys.path.append('D:\pyread')
import MiReadClass as mic

#数据文件夹
forder='D:\\学校\\1大三\\天诊\\sd\\sd\\micaps\\t-td\\500\\'
#数据
file='13052520.000'
#输出文件夹
ofile='D:\pyread\output\\'
ldc=mic.MiR4(forder,file,ofile)
ldc.OutPutContou()
