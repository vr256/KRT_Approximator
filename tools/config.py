from enum import Enum
from functools import partial

import tensorflow as tf
from numpy.polynomial.chebyshev import Chebyshev
from numpy.polynomial.hermite import Hermite
from numpy.polynomial.laguerre import Laguerre
from numpy.polynomial.legendre import Legendre

PATH_LIGHT = 'image/image_light.png'
PATH_DARK = 'image/image_dark.png'

SEARCH_ICON = 'image/search_icon.png'


class Locale(Enum):
    ENG = 'locales/eng.json'
    UKR = 'locales/ukr.json'


class Optimizer(Enum):
    Adam = tf.optimizers.Adam
    SGD = tf.optimizers.SGD
    Nesterov = partial(tf.optimizers.SGD, nesterov=True)
    RMSprop = tf.optimizers.RMSprop
    Adagrad = tf.optimizers.Adagrad


class Polynomial(Enum):
    Hermite = Hermite
    Legendre = Legendre
    Laguerre = Laguerre
    Chebyshev = Chebyshev
