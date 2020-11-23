# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:06:48 2020

@author: tgm
"""

import numpy as np
from dateutil.parser import *
import scipy.ndimage as sn
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import math
import pandas as pd
from sympy.vector import CoordSys3D, divergence
from matplotlib import cm
#import cartopy.crs as ccrs

import numpy as np
import xarray as xr
import scipy.ndimage as ndimage
import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.interpolate import cross_section
from metpy.units import units


# Creating the class
class MicapsOp:
    
    
    # Initialize the class
    def __init__(self,forder,file,ofile):
        self.forder =forder
        self.file=file
        self.ofile=ofile
        
    def getraw(self):
        file_name=self.forder+self.file
        self.raw=np.loadtxt(file_name,dtype=np.str,delimiter='/n')
        self.raw=' '.join(self.raw.tolist())
        self.raw=self.raw.split()
        return self.raw
    
    def DrawContour(self):
        fig,ax = plt.subplots(figsize=(14,9))
    
        m = Basemap(projection='cyl',
                llcrnrlat=self.end_lat, urcrnrlat=self.start_lat,
                llcrnrlon=self.start_lon, urcrnrlon=self.end_lon,
                resolution='l')
        m.drawcoastlines(linewidth=0.8, color='black')
    
        lon=np.linspace(self.start_lon,self.end_lon,self.xsize)
        lat=np.linspace(self.end_lat,self.start_lat,self.ysize)[::-1]               
        lons, lats = np.meshgrid(sn.zoom(lon, self.factor), sn.zoom(lat, self.factor))
        x, y = m(lons, lats)
        c1=m.contour(x,y,sn.zoom(self.data, self.factor),
                 levels=np.arange(self.start_level,self.end_level+self.lineint,self.lineint),colors='r',zorder=1)
        ax.clabel(c1, fmt='%d', inline= True, fontsize=12, inline_spacing=8)
            
        m.readshapefile('D:\\shp\\国界\\国界\\country1', 'province',color='k',linewidth=0.6,zorder=0)
            
        plt.title('%s      Level:%d'%(self.file_time.strftime('%Y-%m-%d %H:%M'),self.level),size=14, loc='left')
        plt.savefig(self.ofile+self.file+'.png',dpi=300,bbox_inches='tight')
    
class MiR4(MicapsOp):
    title =None
    def __init__(self,forder,file,ofile,kind):
        MicapsOp.__init__(self,forder,file,ofile)
        MicapsOp.getraw(self)
        self.kind=kind
        
    def PreData(self):
        self.raw=MicapsOp.getraw(self)
        self.title=self.raw[:3]
        self.time_str='20'+'-'.join(self.raw[3:3+4])
        self.file_time=parse(self.time_str)
        self.duration,self.level=int(self.raw[7]),int(self.raw[8])
        self.xint,self.yint=float(self.raw[9]),float(self.raw[10])
        self.start_lon,self.end_lon=float(self.raw[11]),float(self.raw[12])
        self.start_lat,self.end_lat=float(self.raw[13]),float(self.raw[14])
        self.xsize,self.ysize=int(self.raw[15]),int(self.raw[16])
        self.lineint,self.start_level,self.end_level=int(self.raw[17]),int(self.raw[18]),int(self.raw[19])
        self.smooth,self.boldlevel=int(self.raw[20]),self.raw[21]
    
        self.predata=np.array(self.raw[22:],dtype=float).reshape(self.ysize,self.xsize)
        if self.smooth:
            self.factor=6
        else:
            self.factor=1
        
    def CulVa(self):
        if self.kind=="t-td":
            MiR4.Cultd(self)
        elif self.kind=="pt 500":
            MiR4.Culpt1(self)
        elif self.kind=="pt 850":
            MiR4.Culpt2(self)
        
                  
    def Cultd(self):
        self.data=self.predata
    
    def Culpt1(self):
        self.data=(self.predata)*(1000/500)**0.286
    
    def Culpt2(self):
        self.data=(self.predata)*(1000/850)**0.286
    
        
        
    
    def OutPutContour(self):
        MiR4.PreData(self)
        MiR4.CulVa(self)
        MicapsOp.DrawContour(self)
        
class MiR11(MicapsOp):
    title =None
    def __init__(self,forder,file,ofile):
        MicapsOp.__init__(self,forder,file,ofile)
        MicapsOp.getraw(self)
        
    def PreData(self):
        self.raw=MicapsOp.getraw(self)
        self.title=self.raw[:3]
        self.time_str='20'+'-'.join(self.raw[3:3+4])
        self.file_time=parse(self.time_str)
        self.duration,self.level=int(self.raw[7]),int(self.raw[8])
        self.xint,self.yint=float(self.raw[9]),float(self.raw[10])
        self.start_lon,self.end_lon=float(self.raw[11]),float(self.raw[12])
        self.start_lat,self.end_lat=float(self.raw[13]),float(self.raw[14])
        self.xsize,self.ysize=int(self.raw[15]),int(self.raw[16])
    
        self.datau=np.array(self.raw[17:1554],dtype=float).reshape(self.ysize,self.xsize)
        self.datav=np.array(self.raw[1554:3091],dtype=float).reshape(self.ysize,self.xsize)
        self.factor=6
        
        '''
    def OutPutContour(self):
        MiR11.PreData(self)
       '''
class Eqpt(MicapsOp):
    r=range(-1000,1000,50)
    def __init__(self,file,ofile,p,t,td):
        self.file=file
        self.ofile=ofile
        self.p=p
        self.t=t
        self.td=td
        
        
    def Culw(self):
        Eqpt1=MiR4(self.t,self.file,self.ofile,"t") 
        Eqpt1.PreData()
        self.tda=Eqpt1.predata
        
        Eqpt2=MiR4(self.td,self.file,self.ofile,'td') 
        Eqpt2.PreData()
        self.tdda=Eqpt2.predata
        
        
        self.nameless=(273.16+self.tda)/(273.16+self.tda-(self.tdda))
        for i in range(len(self.nameless)):
            for j in range(len(self.nameless[i])):               
                self.nameless[i,j]=math.log(self.nameless[i,j],2.71828182846)
        self.l=597.3-0.566*self.tda
        self.tl=(0.622*(self.l)*(273.16+Eqpt1.predata-(Eqpt2.predata)))/(0.622*(self.l)+(0.24*(273.16+Eqpt1.predata-(Eqpt2.predata)))*self.nameless)        
        self.nameless1=17.2693882*(Eqpt1.predata-(Eqpt2.predata))/(273.16+(Eqpt1.predata-(Eqpt2.predata)-35.86))
        for i in range(len(self.nameless1)):
            for j in range(len(self.nameless1[i])):
                self.nameless1[i,j]=math.exp(self.nameless1[i,j])
        self.e=6.1078*self.nameless1
        self.q=0.622*self.e/(self.p-0.378*self.e)
        self.nameless2=self.l*self.q/(0.24*self.tl)
        for i in range(len(self.nameless2)):
            for j in range(len(self.nameless2[i])):
                self.nameless2[i,j]=math.exp(self.nameless2[i,j])
        self.data=(273.16+Eqpt1.predata)*((1000/(self.p-self.e))**0.286)
        
        #np.power(self.data,0.286)
        self.data=self.data*self.nameless2
        self.OutPutContour(Eqpt1,self.r)
        
    def OutPutContour(self,e,r):
        
        fig,ax = plt.subplots(figsize=(14,9))
    
        m = Basemap(projection='cyl',
                llcrnrlat=e.end_lat, urcrnrlat=e.start_lat,
                llcrnrlon=e.start_lon, urcrnrlon=e.end_lon,
                resolution='l')
        m.drawcoastlines(linewidth=0.8, color='black')
    
        lon=np.linspace(e.start_lon,e.end_lon,e.xsize)
        lat=np.linspace(e.end_lat,e.start_lat,e.ysize)[::-1]               
        lons, lats = np.meshgrid(sn.zoom(lon, e.factor), sn.zoom(lat, e.factor))
        x, y = m(lons, lats)
        c1=m.contour(x,y,sn.zoom(self.data, e.factor),r,colors='r',zorder=1)
        ax.clabel(c1, fmt='%d', inline= True, fontsize=12, inline_spacing=8)
            
        m.readshapefile('D:\\shp\\国界\\国界\\country1', 'province',color='k',linewidth=0.6,zorder=0)
            
        plt.title('%s      Level:%d'%(e.file_time.strftime('%Y-%m-%d %H:%M'),e.level),size=14, loc='left')
        plt.savefig(self.ofile+self.file+'.png',dpi=300,bbox_inches='tight')
            
class Vert(MicapsOp):
    r=range(-10000,10000,1)
    def __init__(self,file,ofile,p,u):
        self.file=file
        self.ofile=ofile
        self.p=p
        self.u=u
                
    def Sped(self):
        Vert=MiR11(self.u,self.file,self.ofile) 
        Vert.PreData()
        #涡度
        self.uda=units('m/s') *Vert.datau
        #self.uda=Vert.datau
        self.vda=units('m/s') *Vert.datav
        lon=np.linspace(Vert.start_lon,Vert.end_lon,Vert.xsize)
        lat=np.linspace(Vert.end_lat,Vert.start_lat,Vert.ysize)[::-1]
        dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat)
        self.vort = mpcalc.vorticity(self.uda, self.vda,dx,dy)
        self.dive = mpcalc.divergence(self.uda, self.vda,dx,dy)
        self.data=self.vort.magnitude*1e5
        self.OutPutContour(Vert,self.r)
        '''
        涡度平流
        dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat)

        f = mpcalc.coriolis_parameter(np.deg2rad(lat)).to(units('1/sec'))

        avor = mpcalc.vorticity(self.uda, self.vda, dx, dy, dim_order='yx')

        self.data = ndimage.gaussian_filter(avor, sigma=3, order=0) * units('1/s')
        '''
        #散度
        
        #self.OutPutContour(Vert,self.r)
        
    def OutPutContour(self,e,r):
        
        fig,ax = plt.subplots(figsize=(14,9))
    
        m = Basemap(projection='cyl',
                llcrnrlat=e.end_lat, urcrnrlat=e.start_lat,
                llcrnrlon=e.start_lon, urcrnrlon=e.end_lon,
                resolution='l')
        m.drawcoastlines(linewidth=0.8, color='black')
    
        lon=np.linspace(e.start_lon,e.end_lon,e.xsize)
        lat=np.linspace(e.end_lat,e.start_lat,e.ysize)[::-1]               
        lons, lats = np.meshgrid(sn.zoom(lon, e.factor), sn.zoom(lat, e.factor))
        x, y = m(lons, lats)
        c1=m.contour(x,y,sn.zoom(self.data, e.factor),r,colors='r',zorder=1)
        ax.clabel(c1, fmt='%d', inline= True, fontsize=12, inline_spacing=8)
            
        m.readshapefile('D:\\shp\\国界\\国界\\country1', 'province',color='k',linewidth=0.6,zorder=0)
            
        plt.title('%s      Level:%d'%(e.file_time.strftime('%Y-%m-%d %H:%M'),e.level),size=14, loc='left')
        plt.savefig(self.ofile+self.file+'.png',dpi=300,bbox_inches='tight')
        
        
        '''
        #self.uda=self.uda.tolist()
        self.uu=np.diff(self.uda)
        self.vv=np.diff(self.vda,axis=0)
        self.div=self.uu[-1:,:]/2.5+self.vv[:,:-1]
        '''
        
        '''
        self.w=self.uda+2.5
        for i in range (len(self.uda)-1):
            for j in range (len(self.uda[i])-1):
                self.w[i,j]=((self.uda[i+1,j]-self.uda[i,j])/2.5)+(self.vda[i,j+1]-self.vda[i,j])
                
                divergence
                
                W=(((Vert2.CulVa[i+1:j]-Vert2.CulVa[i:j])/(Vert1.CulVa[i+1:j]-Vert1.CulVa[i:j]))\
                    +(Verts3.datau[i,j]*(Vert2.CulVa[i+1:j]-Vert2.CulVa[i:j])/Vert2.xint)\
                    +(Verts3.datav[i,j]*(Vert2.CulVa[i+1:j]-Vert2.CulVa[i:j])/Vert2.yint))/(-1*(Vert2.CulVa[i+1:j]-Vert2.CulVa[i:j])/500)                    
                PT=(Vert1.CulVa[i:j]-Vert1a.CulVa[i:j])/86400
                VT=(Vert2.datau[i,j]*(Vert1.CulVa[i+1:j]-Vert1.CulVa[i:j])/Vert1.xint)+(Vert2.datav[i,j]*(Vert1.CulVa[i:j+1]-Vert1.CulVa[i:j])/Vert1.yint)
        

        R = CoordSys3D('R')
        v1 = R.x*R.y*R.z * (R.i+R.j+R.k)
        divergence(v1)
        v2 = 2*R.y*R.z*R.j
        divergence(v2)
        '''
class Tadv(MicapsOp):
    r=range(-100,100,1)
    def __init__(self,file,ofile,p,u,t):
        self.file=file
        self.ofile=ofile
        self.p=p
        self.u=u
        self.t=t
        
    def Adve(self):
        Tadv1=MiR11(self.u,self.file,self.ofile) 
        Tadv1.PreData()
        Tadv2=MiR4(self.t,self.file,self.ofile,'t') 
        Tadv2.PreData()
        self.uda=Tadv1.datau
        self.vda=Tadv1.datav
        self.t  =Tadv2.predata
        
        lon=np.linspace(Tadv2.start_lon,Tadv2.end_lon,Tadv2.xsize)
        lat=np.linspace(Tadv2.end_lat,Tadv2.start_lat,Tadv2.ysize)[::-1]
        dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat)
        self.adv = mpcalc.advection(self.t,[self.uda,self.vda],
                       (dx, dy), dim_order='yx')
        #print(self.adv)
        self.data=self.adv*1e6
        print(self.data)
        self.OutPutContour(Tadv2,self.r)

    def OutPutContour(self,e,r):
        
        fig,ax = plt.subplots(figsize=(14,9))
    
        m = Basemap(projection='cyl',
                llcrnrlat=e.end_lat, urcrnrlat=e.start_lat,
                llcrnrlon=e.start_lon, urcrnrlon=e.end_lon,
                resolution='l')
        m.drawcoastlines(linewidth=0.8, color='black')
    
        lon=np.linspace(e.start_lon,e.end_lon,e.xsize)
        lat=np.linspace(e.end_lat,e.start_lat,e.ysize)[::-1]               
        lons, lats = np.meshgrid(sn.zoom(lon, e.factor), sn.zoom(lat, e.factor))
        x, y = m(lons, lats)
        c1=m.contourf(x,y,sn.zoom(self.data, e.factor),r,zorder=1,cmap=cm.jet)
        ax.clabel(c1, fmt='%d', inline= True, fontsize=12, inline_spacing=8)
            
        m.readshapefile('D:\\shp\\国界\\国界\\country1', 'province',color='k',linewidth=0.6,zorder=0)
            
        plt.title('%s      Level:%d'%(e.file_time.strftime('%Y-%m-%d %H:%M'),e.level),size=14, loc='left')
        plt.savefig(self.ofile+self.file+'.png',dpi=300,bbox_inches='tight')        
            
            
        
         
         
         
         
    


