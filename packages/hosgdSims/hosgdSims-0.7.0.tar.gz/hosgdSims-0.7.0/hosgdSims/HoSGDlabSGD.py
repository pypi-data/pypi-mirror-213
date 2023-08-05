

import numpy as np
import scipy as sc
from scipy import signal

from scipy.special import softmax,logsumexp

import matplotlib.pylab as PLT
from matplotlib.ticker import MaxNLocator

import HoSGDdefs as hosgdDef
from HoSGDdefs import hosgdOptProb

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Disbales TF's warnings (they don' shown in generated HTML)

# Note: TF is used to have a simple access to MNIST
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.datasets import cifar10


class hosgdHyperFunSGD(object):
    r"""Class related to routines associated to hyperPars computation
    """

    def __init__(self, lrPolicy=hosgdDef.lrSGD.Cte, lrSDecay=20, lrTau = 0.5):
        self.lrPolicy = lrPolicy
        self.LR   = self.sel_LR()
        self.lrSDecay = lrSDecay
        self.lrTau    = lrTau

    def sel_LR(self):
      switcher = {
          hosgdDef.lrSGD.Cte.val:        self.lrCte,
          hosgdDef.lrSGD.StepDecay.val:  self.lrStepDecay,
          }

      lrFun = switcher.get(self.lrPolicy.val, "nothing")

      func = lambda u, alpha, k, g: lrFun(u, alpha, k, g)

      return func

    # --- === ---

    def lrCte(self, u, alpha, k, g):
        return alpha

    # --- === ---

    def lrStepDecay(self, u, alpha, k, g):
        return (self.lrTau**np.floor(k/self.lrSDecay))*alpha


# ===========================================

class hosgdFunSoftMax(hosgdOptProb):
    r""" F(W)   = (1/N) \sum_n f_n(W)
         f_n(W) = < Xn, Wl_n > + log( \sum_l e^{ -< Xl, Wl >} )
    """

    def __init__(self, X, Y, nClass, Xtest=None, Ytest=None, lmbd=0,
                 gNormOrd=2, Nstats=5, verbose=10, initSol=None):

        self.X = X
        self.Y = Y
        self.nClass = nClass
        self.Xtest = Xtest
        self.Ytest = Ytest
        self.lmbd = lmbd
        self.Nstats   = Nstats
        self.gNormOrd = gNormOrd
        self.verbose  = verbose
        self.initSol  = initSol      #  if not None --> reproducible initial solution


    # ---------

    def costFun(self, W):

        fCost = np.sum(np.log(np.sum(np.exp(-self.X.transpose().dot(W)), axis=1)))
        fCost += np.sum( self.X*W[:,self.Y] )

        fCost /= float(self.X.shape[1])

        if self.lmbd > 0:
           fCost += self.lmbd*(sum( np.power(W.ravel(),2) ))/float(self.X.shape[1])

        return fCost


    # ---------

    def fwOp(self, W):

        return None

    # ---------

    def gradFun(self, W, n):

        z = self.X[:,np.ix_(n)].squeeze(1)      # select batch elements

        g = -z.dot( softmax(-z.transpose().dot(W),axis=1) )

        for k in range(len(n)):
            g[:,self.Y[n[k]] ] += z[:,k]

        g /= float(len(n))

        if self.lmbd > 0:
            g += self.lmbd*W

        return g

    # ---------

    def randSol(self):

        if self.initSol is None:
           rng = np.random.default_rng()
        else:
           rng = np.random.default_rng(self.initSol)

        return 0.01*rng.normal(size=[self.X.shape[0], self.nClass] )



    # ---------

    def computeStats(self, W, alpha, k, g):

        cost  = self.costFun(W)

        gNorm = self.gradNorm(g, self.gNormOrd)

        success = self.computeSuccess(W)

        return np.array([k, cost, alpha, gNorm, success])

    # ---------

    def computeSuccess(self, W):

        if self.Xtest is not None and self.Ytest is not None:
            classVal = -np.matmul(self.Xtest.transpose(), W)
            success = sum( np.argmax(classVal,axis=1) == self.Ytest )

            return float(success)/float(self.Xtest.shape[1])
        else:
            return None

    # ---------

    def printStats(self, k, nEpoch, v):

        if k == 0:
            print('\n')

        if self.verbose > 0:

            if np.remainder(k,self.verbose)==0 or k==nEpoch-1:
                if v[k,4] is None:
                    print('{:>3d}\t {:.3e}\t {:.2e}    {:.2e}'.format(int(v[k,0]),v[k,1],v[k,2],v[k,3]))
                else:
                    print('{:>3d}\t {:.3e}\t {:.2e}    {:.2e}\n \t \
                          success rate (training): {:.3e}'.format(int(v[k,0]),v[k,1],v[k,2],v[k,3],v[k,4]))

        return

    # ---------

    def gradNorm(self, g, ord=2):

        if g is None:
           return -1.0

        if ord == 2:
            return np.linalg.norm(g.ravel(),ord=ord)**ord
        else:
            return np.linalg.norm(g.ravel(),ord=ord)

# ===========================================


def hosgdSGD(OptProb, nEpoch, blkSize, alpha0, hyperFun):

    W = OptProb.randSol()

    stats = np.zeros( [nEpoch, OptProb.Nstats] )

    nBlk = np.floor_divide(OptProb.X.shape[1],blkSize)
    if np.remainder(OptProb.X.shape[1],blkSize) > 0:
       nBlk += 1

    k = 0

    for e in range(nEpoch):

      # Generate permutation
      blkInd = 0
      perm = np.random.permutation(OptProb.X.shape[1])

      for b in range(nBlk):

        # general iteration counter
        k += 1

        # select indexes
        if b <= nBlk-2:
           n = perm[blkInd:blkInd+blkSize]
        else:
           n = perm[blkInd:OptProb.X.shape[1]]

        blkInd += blkSize

        # Compute the gradient
        g     = OptProb.gradFun(W, n)

        alpha = hyperFun.LR(W, alpha0, e, None)

        W = W - alpha*g

        # _END_ for(b)

      stats[e,:] = OptProb.computeStats(W, alpha, e, g)
      OptProb.printStats(e, nEpoch, stats)


    return W, stats



def stdPreproc(dIn, L=255.0, flagNorm=True, flagMean=True):

    dIn = dIn.astype("float")

    if flagNorm:
       dIn = dIn/L

    if flagMean:
       mean = np.mean(dIn, axis = 0)
       dIn -= mean

    return(dIn)


def exMultiClass(nEpoch, blkSize, alpha, dataset='mnist', lrPolicy=hosgdDef.lrSGD.Cte, lrSDecay=20, lrTau = 0.5, verbose=5):

    # Examples
    #  w, stats = H.exMultiClass(20, 32, 0.05, dataset='mnist')
    #  w, stats = H.exMultiClass(20, 32, 0.01, dataset='cifar10')
    #  w, stats = H.exMultiClass(25, 64, 0.02, dataset='cifar10', lrPolicy=hosgdDef.lrSGD.StepDecay, lrSDecay=10, lrTau=0.5)

    # --- Load data
    # -------------------

    flagDataset = False

    if dataset.lower() == 'mnist':
       (X, Y), (Xtest, Ytest) = mnist.load_data()
       flagDataset = True

    if dataset.lower() == 'cifar10':
       (X, Y), (Xtest, Ytest) = cifar10.load_data()
       flagDataset = True

    if flagDataset is False:
       print('Dataset {} is no valid'.format(dataset))
       return

    if verbose == 1:
       print('Shape (training data):', X.shape)
       print('Shape (valid/testing data):', Xtest.shape)
       print('\n')

    # pre-processing
    X     = stdPreproc(X)
    Xtest = stdPreproc(Xtest)


    # Data vectorization
    X     = np.transpose( X.reshape(X.shape[0], np.array(X.shape[1::]).prod()) )
    Xtest = np.transpose( Xtest.reshape(Xtest.shape[0], np.array(Xtest.shape[1::]).prod()) )
    Y     = Y.ravel()
    Ytest = Ytest.ravel()

    # --- Optimization model
    # ----------------------

    OptProb = hosgdFunSoftMax(X, Y, 10, verbose=verbose, Xtest=Xtest, Ytest=Ytest)


    # --- HyperPar (this is kept in order to have a similar structure to the SD case (see Lab 1a)
    # ------------

    hyperP = hosgdHyperFunSGD(lrPolicy=lrPolicy, lrSDecay=lrSDecay, lrTau=lrTau)

    # --- Call GD
    # -----------
    W, stats = hosgdSGD(OptProb, nEpoch, blkSize, alpha, hyperP)


    # --- Plot results
    # ----------------

    plotSGDStats(stats)

    return W, stats




def plotSGDStats(stats):

  # --- Plot results ---

  ax = PLT.figure().gca()
  ax.xaxis.set_major_locator(MaxNLocator(integer=True))

  PLT.plot(stats[:,1] )
  PLT.ylabel('Softmax', fontsize=16)
  PLT.xlabel('Epoch', fontsize=16)
  PLT.title('Loss function', fontsize=20)

  if stats[0,4] is not None:

    ax = PLT.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    PLT.plot(stats[:,4] )
    PLT.ylabel('Accuracy', fontsize=16)
    PLT.xlabel('Epoch', fontsize=16)
    PLT.title('Success rate (test)', fontsize=20)

  PLT.show()




