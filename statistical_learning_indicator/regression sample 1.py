import numpy as np
import scipy.interpolate as sc
import matplotlib.pyplot as plt


x = np.array([0,1,2,3,4,5])
y = np.array([0,0.8,0.9,0.1,-0.8,-1])

print(x,y)
p1 = np.polyfit (x,y,1)
p2 = np.polyfit (x,y,2)     # x, x^2, y
p3 = np.polyfit (x,y,3)     # x, x^2, x^3, y

a = plt.plot(x,y,'o')
#plt.show(a)

a1 = plt.plot(x, np.polyval(p1,x),'r-')     # fits red line to data
a2 = plt.plot(x, np.polyval(p2,x),'b-')
a3 = plt.plot(x, np.polyval(p3,x),'m:')
plt.show()


print(p1,p2,p3)
