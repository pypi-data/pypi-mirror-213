from enum import Enum, IntEnum, unique

@unique
class ss(Enum):
  Cte            = (0, 'Cte step-size')
  Cauchy         = (1, 'Cauchy')
  CauchyLagged   = (2, 'Cauchy-BB (lagged)')
  CauchyRand     = (3, 'Cauchy rand')
  CauchySupp     = (4, 'Cauchy supp')
  CauchyLSupp    = (5, 'Cauchy-BB supp')
  BBv1           = (6, 'BBv1')
  BBv2           = (7, 'BBv2')
  BBv3           = (8, 'BBv3')

  def __init__(self, val, txt):
      self.val  = val
      self.txt  = txt

  @classmethod
  def printSS(cls):
      for k in cls:
        print('ss.{}:'.format(k.name), k.val, k.txt)


@unique
class lrSGD(Enum):
  Cte            = (0, 'Cte lerning rate')
  StepDecay      = (1, 'StepDecay')

  def __init__(self, val, txt):
      self.val  = val
      self.txt  = txt

  @classmethod
  def printLR(cls):
      for k in cls:
        print('lrSGD.{}:'.format(k.name), k.val, k.txt)


@unique
class iseq(Enum):
  Ntrv           = (0, 'Standard ISeq')
  Lin            = (1, 'Linear ISeq')
  GLin           = (1, 'Generalized linear ISeq')

  def __init__(self, val, txt):
      self.val  = val
      self.txt  = txt

  @classmethod
  def printLR(cls):
      for k in cls:
        print('iseq.{}:'.format(k.name), k.val, k.txt)


@unique
class actFun(Enum):
  ReLU          = (0, 'ReLU')
  RReLU         = (1, 'Rand ReLU')
  ELU           = (2, 'ELU')

  def __init__(self, val, txt):
      self.val  = val
      self.txt  = txt

  @classmethod
  def printLR(cls):
      for k in cls:
        print('actFun.{}:'.format(k.name), k.val, k.txt)


@unique
class hlFun(Enum):
  dense         = (0, 'Dense (matrix times)')

  def __init__(self, val, txt):
      self.val  = val
      self.txt  = txt

  @classmethod
  def printLR(cls):
      for k in cls:
        print('hlFun.{}:'.format(k.name), k.val, k.txt)


# ===========================================

class hosgdOptProb(object):
    r"""Simple class to describe the attributtes of an optimization problem

    """

    def __init__(self):
        pass

    def costFun(self, u):
        pass

    def gradFun(self, u):
        pass


    def randSol(self):
        return None


    def gradNorm(self, g, ord=2):
        return None


# ===========================================

