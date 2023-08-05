import numpy as np
import matplotlib.pylab as PLT

def ReLU(u):
  return np.maximum(u,0)

def plotReLU(val=5, dpoints=100):

  x = np.linspace(-val,val,dpoints)
  xReLU = ReLU(x)

  ax = PLT.figure().gca()

  PLT.plot(x, xReLU)
  PLT.title('ReLU Activation Function')
  PLT.show()


