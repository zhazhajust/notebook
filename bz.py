import sdf
import numpy as np
import constant as const
from mayavi import mlab
data=sdf.read('Documents/data/2800.sdf',dict=True)
var1  = data['Electric Field/Ey'].data
bz=var1
k_bz=np.fft.fft(bz,axis=0)
delta_k=3.14/const.delta_x/(const.Nx/2)
k_bz2=k_bz*1
k_n=[]
for n in range(0,const.Nx):
	mi = 3e8/0.1e12#limit_min
	ma = 3e8/10e12#limit_max
	if 2 * 3.14 / ma  > n * delta_k and  n * delta_k > 2 * 3.14 / mi:
		k_n.append(n)
k_bz2[0:k_n[0],:,:]=0    #k_bz.argmin()
k_bz2[k_n[-1]:-k_n[-1],:,:]=0  #k_bz.argmin()
k_bz2[-k_n[0]:,:,:]=0    #k_bz.argmin()
var1=np.fft.ifft(k_bz2,axis=0).real
mlab.contour3d(var1)
mlab.show()
