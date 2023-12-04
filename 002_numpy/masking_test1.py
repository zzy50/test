import numpy as np
import matplotlib.pyplot as plt

y,x=np.mgrid[0:1000,0:1000]

#a wiggly ramp
plt.subplot(221)
mask0=(y < x + 20 * np.sin(0.05*x)) & (y > x - 100 + 20 * np.sin(0.05*x))
plt.imshow(mask0,origin='lower',cmap='gray')

#a ramp
plt.subplot(222)
mask1=(y < x) & (x < y+100)
plt.imshow(mask1,origin='lower',cmap='gray')

#a disk
plt.subplot(223)
mask2=(200**2>(x-500)**2+(y-500)**2)
plt.imshow(mask2,origin='lower',cmap='gray')

#a ying-yang attempt
plt.subplot(224)
mask3= (mask2 & (0 < np.sin(3.14*x/250)*100 + 500 - y) & (30**2 < (x-620)**2+(y-500)**2) )| (30**2 > (x-380)**2+(y-500)**2)
plt.imshow(mask3,origin='lower',cmap='gray')

plt.show()