# -- coding: utf-8 --
import sdf
import matplotlib
import math
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from numpy import ma
from matplotlib import colors, ticker, cm
from matplotlib.mlab import bivariate_normal
from scipy.interpolate import spline
  
if __name__ == "__main__":
  ######## Constant defined here ########
  pi        =     3.1415926535897932384626
  q0        =     1.602176565e-19 # C
  m0        =     9.10938291e-31  # kg
  v0        =     2.99792458e8    # m/s^2
  kb        =     1.3806488e-23   # J/K
  mu0       =     4.0e-7*pi       # N/A^2
  epsilon0  =     8.8541878176203899e-12 # F/m
  h_planck  =     6.62606957e-34  # J s
  wavelength=     1.0e-6
  frequency =     v0*2*pi/wavelength
  micron    =     1.0e-6
  c         =     3e8
  exunit    =     m0*v0*frequency/q0
  bxunit    =     m0*frequency/q0
  denunit    =     frequency**2*epsilon0*m0/q0**2
  print 'electric field unit: '+str(exunit)
  print 'magnetic field unit: '+str(bxunit)
  print 'density unit nc: '+str(denunit)
  
  font = {'family' : 'monospace',  
          'color'  : 'black',  
          'weight' : 'normal',  
          'size'   : 28,  
          }  
  
  
  
  ######### Parameter you should set ###########
  start   =  1  # start time
  stop    =  1000  # end time
  step    =  1  # the interval or step
  
  if (os.path.isdir('fft') == False):
    os.mkdir('fft')
  if (os.path.isdir('txt') == False):
    os.mkdir('txt')
  ######### Script code drawing figure ################
  t = []
  bz = []
####################
  #x0 = 50*80 + 100
  #y0 = 30*100 + 100
  #d  = 30.0

  #theta = -pi*30.0/180.0
  #x = x0 + int(50.0*d*math.cos(theta))
  #y = y0 + int(30.0*d*math.sin(theta))
  y=0
  e=[]
  e2= []
  t2=[]
  bz2=[]
  #print x,y
  delta_x = 61*micron/1500
  '''for x in range(int(500*micron/delta_x)):
    print "x:"
    print x
    e=[]
    t=[]
    bz=[]'''
  t=[]
  bz=np.zeros((7377,1000)) 
  for n in range(start,stop+step,step):
        #### header data ####
        data = sdf.read("./Data/new/"+str(n).zfill(4)+".sdf",dict=True)
        header=data['Header']
        time=header['time']
        t.append(header['time']*1e15) #[fs]
        n=int(time/1e-15)
        for x in range(7377):
           if x > 1500:
             if int(x-c*time/delta_x) > 0 and int(x-c*time/delta_x) < 1500:
              t.append(header['time']*1e15) #[fs]
   
              bz[x][n]=data['Magnetic Field/Bz'].data[int(x-c*time/delta_x)][y]/bxunit
             #else:bz.append(0)
             #print 'Reading finished%d' %len(t)
  N0 = len(bz[1])		##取样长度
  T = t[len(t)-1]-t[0]		##时间间隔
  fs = N0*1e3/T		##取样频率[THz]
  freqs=[]
  xf=np.zeros((7377,1000))

  freqs = np.linspace(0, fs/2, N0/2+1)
  for x in range(int(5080*micron/delta_x)):
    xf[x] = np.fft.rfft(bz[x])/N0
    #xf[0] = xf[0]/2
    #xf[N0/2] = xf[N0/2]/2

    xf=np.abs(xf)
  
  np.savetxt("./txt/bz.txt", bz)
  np.savetxt("./txt/t.txt", t)

  np.savetxt("./txt/freqs.txt", frees)
  np.savetxt("./txt/xf.txt", xf)
