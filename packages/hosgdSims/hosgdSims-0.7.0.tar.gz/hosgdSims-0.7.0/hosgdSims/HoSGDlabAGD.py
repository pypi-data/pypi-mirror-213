import numpy as np
import scipy as sc
from scipy import signal

import matplotlib.pylab as PLT

import HoSGDdefs as hosgdDef

from HoSGDlabGD import hosgdFunQlin, hosgdHyperFun, hosgdGD, plotGDDictStats


class hosgdHyperFunAGD(hosgdHyperFun):
    r"""Class (child) related to routines associated to hyperPars computation
    """

    def __init__(self, OptProb, ssPolicy=hosgdDef.ss.Cte, iseqPolicy=hosgdDef.iseq.Ntrv, mtmGamma=0.9, iseqPar1=2,iseqPar2=80):
        self.ssPolicy = ssPolicy
        self.iseqPolicy = iseqPolicy
        self.fwOp = OptProb.fwOp
        self.SS   = self.sel_SS()
        self.ISeq = self.sel_ISeq()
        self.mtmGamma = mtmGamma
        self.iseqPar1 = iseqPar1
        self.iseqPar2 = iseqPar2

    # --- === ---

    def sel_ISeq(self):
      switcher = {
          hosgdDef.iseq.Ntrv.val:   self.iseqNtrv,
          hosgdDef.iseq.Lin.val:    self.iseqLin,
          hosgdDef.iseq.GLin.val:   self.iseqGlin,
          }

      iseqFun = switcher.get(self.iseqPolicy.val, "nothing")

      func = lambda k: iseqFun(k)

      return func

    # --- === ---

    def iseqNtrv(self, k):

        if k == 0:
           self.t0 = 1.0

        self.t1 = 0.5 * float(1. + np.sqrt(1. + 4. * self.t0**2.))
        gamma = (self.t0-1.)/self.t1
        self.t0 = self.t1

        return gamma


    def iseqLin(self, k):

        gamma = ((k+1.)-1.)/( ((k+1.)-1.) + self.iseqPar1 + 1)

        return gamma


    def iseqGlin(self, k):

        gamma = ((k+1.)-1. -(1+self.iseqPar1) + self.iseqPar2 )/((k+1.) + self.iseqPar1  )

        return gamma



def hosgdMTM(OptProb, nIter, alpha0, hyperFun):

    u = OptProb.randSol()
    z = 0*u
    stats = np.zeros( [nIter, OptProb.Nstats] )

    for k in range(nIter):

        g     = OptProb.gradFun(u)

        alpha = hyperFun.SS(u, alpha0, k, g)

        z     = hyperFun.mtmGamma*z - alpha*g

        u = u + z

        stats[k,:] = OptProb.computeStats(u, alpha, k, g)

        OptProb.printStats(k, nIter, stats)

    return u, stats

# ===========================================

def hosgdNTRV(OptProb, nIter, alpha0, hyperFun):

    u1 = OptProb.randSol()
    y  = u1.copy()

    stats = np.zeros( [nIter, OptProb.Nstats] )

    for k in range(nIter):

        g     = OptProb.gradFun(y)

        alpha = hyperFun.SS(u1, alpha0, k, g)
        gamma = hyperFun.ISeq(k)

        u0 = u1.copy()

        u1 = y - alpha*g

        y     = u1 + gamma*(u1 - u0)


        stats[k,:] = OptProb.computeStats(u1, alpha, k, g)

        OptProb.printStats(k, nIter, stats)

    return u1, stats

# ===========================================


def exQlinAGD(nIter, alpha, N=1000, M=500, sigma=0.05, ssPolicy=hosgdDef.ss.Cte, iseqPolicy=None, mtmGamma=None):

    # Examples
    #

    # --- Data generation
    # -------------------
    rng = np.random.default_rng()

    A = rng.normal(size=[N,M])
    D = np.sqrt(max(N,M))*np.diag( rng.random([max(N,M),]), 0)
    A += D[0:N,0:M]
    A /= np.linalg.norm(A,axis=0)

    xOrig = np.random.randn(M,1)

    b = A.dot(xOrig) + sigma*np.random.randn(N,1)

    # --- Optimization model
    # ----------------------

    OptProb = hosgdFunQlin(A,b)

    # --- HyperPar
    # ------------

    if iseqPolicy is None and mtmGamma is None:

        u = []
        stats = []
        ssPlcyList = []
        algoList = []

        # --- ___ ---

        hyperP = hosgdHyperFun(OptProb, ssPolicy=ssPolicy)

        sol = hosgdGD(OptProb, nIter, alpha, hyperP)
        u.append(sol[0])
        stats.append(sol[1])
        ssPlcyList.append( ssPolicy )
        algoList.append('GD')

        # --- ___ ---

        hyperP = hosgdHyperFunAGD(OptProb, ssPolicy=ssPolicy, mtmGamma=0.9)

        sol = hosgdMTM(OptProb, nIter, alpha, hyperP)
        u.append(sol[0])
        stats.append(sol[1])
        ssPlcyList.append( ssPolicy )
        algoList.append('Momentum')

        # --- ___ ---

        hyperP = hosgdHyperFunAGD(OptProb, ssPolicy=ssPolicy, mtmGamma=0.9)

        sol = hosgdNTRV(OptProb, nIter, alpha, hyperP)
        u.append(sol[0])
        stats.append(sol[1])
        ssPlcyList.append( ssPolicy )
        algoList.append('Nesterov')


        stDict = {'stats': stats, 'ssPlcy': ssPlcyList, 'alphaVal': alpha, 'algoList': algoList, 'alphaPlot':False}

        plotAGDDictStats(stDict)

    elif iseqPolicy is None and mtmGamma is not None:

        u = []
        stats = []
        ssPlcyList = []
        algoList = []

        hyperP = hosgdHyperFunAGD(OptProb, ssPolicy=ssPolicy, mtmGamma=mtmGamma)

        sol = hosgdMTM(OptProb, nIter, alpha, hyperP)
        u.append(sol[0])
        stats.append(sol[1])
        ssPlcyList.append( ssPolicy )
        algoList.append('Momentum')

        stDict = {'stats': stats, 'ssPlcy': ssPlcyList, 'alphaVal': alpha, 'algoList': algoList, 'alphaPlot':False}

        plotAGDDictStats(stDict)

    elif iseqPolicy is not None and mtmGamma is None:

        u = []
        stats = []
        ssPlcyList = []
        algoList = []

        hyperP = hosgdHyperFunAGD(OptProb, ssPolicy=ssPolicy, iseqPolicy=iseqPolicy)

        sol = hosgdNTRV(OptProb, nIter, alpha, hyperP)
        u.append(sol[0])
        stats.append(sol[1])
        ssPlcyList.append( ssPolicy )
        algoList.append('Nesterov')


        stDict = {'stats': stats, 'ssPlcy': ssPlcyList, 'alphaVal': alpha, 'algoList': algoList, 'alphaPlot':False}

        plotAGDDictStats(stDict)

    return u, stats



def plotAGDDictStats(stDict):


  stats    = stDict.get('stats')
  ssPlcy   = stDict.get('ssPlcy')
  alpha    = stDict.get('alphaVal')
  algoName = stDict.get('algoList')

  alphaPlot  = stDict.get('alphaPlot')

  # --- Plot cost function ---
  PLT.figure()

  for n in range(len(stats)):
    PLT.semilogy(stats[n][:,1], label=r'$\alpha_k$ : {0} -- {1}, {2}'.format(alpha, algoName[n], ssPlcy[n].txt) )

  PLT.legend(loc='upper right')
  PLT.ylabel(r'$f(x) = \frac{1}{2}\| A \mathbf{x} - \mathbf{b} \|_2^2$', fontsize=16)
  PLT.xlabel('Iteration', fontsize=16)
  PLT.title('Cost functional',fontsize=16)

  # --- Plot SS ---
  if alphaPlot:

    PLT.figure()

    for n in range(len(stats)):
      PLT.plot(stats[n][1::,2], label=r'$\alpha_k$ : {0}'.format(ssPlcy[n].txt) )

    PLT.legend(loc='upper right')
    PLT.ylabel(r'$\alpha$', fontsize=20)
    PLT.xlabel('Iteration', fontsize=16)
    PLT.title('Step-size',fontsize=16)

  # ---

  PLT.show()
