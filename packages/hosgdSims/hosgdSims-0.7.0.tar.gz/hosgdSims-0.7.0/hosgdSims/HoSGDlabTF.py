import numpy as np
import matplotlib.pyplot as PLT
from matplotlib.ticker import MaxNLocator

import os
import IPython

import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow import keras

import keras.backend as K

from tensorflow.python.ops import array_ops, math_ops, state_ops, control_flow_ops


from tensorflow.keras.models import Sequential
from tensorflow.keras.applications.vgg16 import VGG16

from tensorflow.keras.layers import (
    Dense,
    Conv2D,
    MaxPool2D,
    Flatten,
    Dropout,
    BatchNormalization,
)

from tensorflow.keras.datasets import mnist
from tensorflow.keras.datasets import cifar10

import tqdm
import tensorflow_addons as tfa



# ============================================================

# --- TF model ---

def create_SimpleNet(opName, inShape, nClasses):

  model = tf.keras.Sequential([
#
        keras.layers.Flatten(),
#
        keras.layers.Dense(units=512, activation='relu', input_shape=inShape),
#
        keras.layers.Dense(units=nClasses, activation='softmax')

    ])

  model.compile(optimizer=opName,loss='categorical_crossentropy', metrics=['accuracy'],)

  return model

# ============================================================

# --- Utility functions ---

def stdPreproc(dIn,L=255.0, flagNorm=True, flagMean=True):

    dIn = dIn.astype("float")

    if flagNorm:
       dIn = dIn/L

    if flagMean:
       mean = np.mean(dIn, axis = 0)
       dIn -= mean

    return(dIn)


def load_mnist():

    (x_train, y_train), (x_valid, y_valid) = mnist.load_data()

    return (x_train, y_train), (x_valid, y_valid)


def load_cifar10():

    (x_train, y_train), (x_valid, y_valid) = cifar10.load_data()

    return (x_train, y_train), (x_valid, y_valid)

# simple scheduler
def schedulerBLK20(epoch, lr):
  if np.remainder(epoch, 20)!=0 or epoch==0:
    return lr
  else:
    return lr * 0.5

# ============================================================



def HoSGD_testNetwork(lr, nEpoch, blkSize, num_categories=10, modelFun=create_SimpleNet, mtmVal=0.9, epsAdam=1e-8):
#
#  HoSGD_testNetwork(0.001, 50, 128)
#

# ----------
# Read data
# ----------

    (x_train, y_train), (x_valid, y_valid) = load_cifar10()

# pre-processing
    x_train = stdPreproc(x_train)
    x_valid = stdPreproc(x_valid)

# add categories
    y_train = keras.utils.to_categorical(y_train, num_categories)
    y_valid = keras.utils.to_categorical(y_valid, num_categories)


# ----------
# Optimizers
# ----------

    model = []
    HName = []
    callbackList = []

    # SGD
    tfOpt = tf.keras.optimizers.SGD(learning_rate=lr,momentum=0.0,nesterov=False)
    model.append( modelFun(tfOpt, inShape=[x_train.size], nClasses=num_categories ) )
    HName.append('TF SGD - lr {:.3f}'.format(lr))

    callbackList.append( [tfa.callbacks.TQDMProgressBar(leave_epoch_progress=True,show_epoch_progress=False)] )


    # SGD+MTM
    tfOpt = tf.keras.optimizers.SGD(learning_rate=lr,momentum=mtmVal,nesterov=False)
    model.append( modelFun(tfOpt, inShape=[x_train.size], nClasses=num_categories ) )
    HName.append('TF MTM - lr {:.3f}, momentum {:.3f}'.format(lr,mtmVal))

    callbackList.append( [tfa.callbacks.TQDMProgressBar(leave_epoch_progress=True,show_epoch_progress=False)] )


    # Adam
    tfOpt = tf.keras.optimizers.Adam(learning_rate=lr,beta_1=0.9, beta_2=0.999, epsilon=epsAdam)
    model.append( modelFun(tfOpt, inShape=[x_train.size], nClasses=num_categories ) )
    HName.append('TF Adam - lr {:.3f} - $\epsilon$({:.2e})'.format(lr, epsAdam))

    callbackList.append( [tfa.callbacks.TQDMProgressBar(leave_epoch_progress=True,show_epoch_progress=False)] )


    # Adam + sch20
    tfOpt = tf.keras.optimizers.Adam(learning_rate=lr,beta_1=0.9, beta_2=0.999, epsilon=epsAdam)
    model.append( modelFun(tfOpt, inShape=[x_train.size], nClasses=num_categories ) )
    HName.append('TF Adam - lr {:.3f} - $\epsilon$({:.2e}) - sch20'.format(lr, epsAdam))

    callbackList.append( [tfa.callbacks.TQDMProgressBar(leave_epoch_progress=True,show_epoch_progress=False)] )
    callbackList[3].extend( [ tf.keras.callbacks.LearningRateScheduler(schedulerBLK20) ] )

# -------------
# Execute model
# -------------

    print('\n')
    print('==='*5)


    History = {}
    for k in range(len(HName)):
        K.clear_session()
        print('\n')
        print('Training: ',HName[k])
        strategy = tf.distribute.MultiWorkerMirroredStrategy()

        History[HName[k]] = model[k].fit(x_train, y_train, epochs=nEpoch, validation_data=(x_valid, y_valid),
                                         batch_size=blkSize,
                                         verbose=0, callbacks=callbackList[k])

    print('\n')
    print('==='*5)
    print('\n')

    #=====================================
    # Plot results

    plotTFsims(History)

    #=====================================
    # Clean-up

    # For Jupyter
    #app = IPython.Application.instance()
    #app.kernel.do_shutdown(True)

    return History


def plotTFsims(History):

    ax = PLT.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    for k, keys in enumerate(History):
        PLT.plot(History[keys].history['loss'],label=r'{0}'.format(keys))

    PLT.legend(loc='upper right')
    PLT.title('model loss')
    PLT.ylabel('loss')
    PLT.xlabel('epoch')

    # ---

    ax = PLT.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    for k, keys in enumerate(History):
        PLT.plot(History[keys].history['val_accuracy'],label=r'{0}'.format(keys))

    PLT.legend(loc='lower right')
    PLT.title('model accuracy')
    PLT.ylabel('accuracy')
    PLT.xlabel('epoch')

    PLT.show()

