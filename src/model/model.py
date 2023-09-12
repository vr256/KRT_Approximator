from enum import Enum
from functools import partial

import numpy as np
import tensorflow as tf
from numpy.polynomial.chebyshev import Chebyshev, cheb2poly
from numpy.polynomial.hermite import Hermite, herm2poly
from numpy.polynomial.laguerre import Laguerre, lag2poly
from numpy.polynomial.legendre import Legendre, leg2poly


class Locale(Enum):
    ENG = "src/locales/eng.json"
    UKR = "src/locales/ukr.json"

    def translate(option: str):
        match option:
            case "English" | "Англійська":
                return Locale.ENG
            case "Ukrainian" | "Українська":
                return Locale.UKR


class Theme(Enum):
    Light = "Light"
    Dark = "Dark"

    def translate(option: str):
        match option:
            case "Light" | "Світла":
                return Theme.Light
            case "Dark" | "Темна":
                return Theme.Dark


class Optimizer(Enum):
    Adam = tf.optimizers.Adam
    SGD = tf.optimizers.SGD
    Nesterov = partial(tf.optimizers.SGD, nesterov=True)
    RMSprop = tf.optimizers.RMSprop
    Adagrad = tf.optimizers.Adagrad

    def translate(option: str):
        match option:
            case "Adam":
                return Optimizer.Adam
            case "SGD":
                return Optimizer.SGD
            case "Nesterov":
                return Optimizer.Nesterov
            case "RMSprop":
                return Optimizer.RMSprop
            case "Adagrad":
                return Optimizer.Adagrad


class Polynomial(Enum):
    Hermite = Hermite
    Legendre = Legendre
    Laguerre = Laguerre
    Chebyshev = Chebyshev

    def translate(option: str):
        match option:
            case "Hermite" | "Ерміта":
                return Polynomial.Hermite
            case "Legendre" | "Лежандра":
                return Polynomial.Legendre
            case "Laguerre" | "Лаґерра":
                return Polynomial.Laguerre
            case "Chebyshev" | "Чебишова":
                return Polynomial.Chebyshev

    def alias_repr(self):
        match self:
            case Polynomial.Hermite.value:
                return "H"
            case Polynomial.Legendre.value | Polynomial.Laguerre.value:
                return "L"
            case Polynomial.Chebyshev.value:
                return "T"

    def convert(self, x: np.ndarray):
        match self:
            case Polynomial.Hermite.value:
                return herm2poly(self(x).coef)
            case Polynomial.Legendre.value:
                return leg2poly(self(x).coef)
            case Polynomial.Laguerre.value:
                return lag2poly(self(x).coef)
            case Polynomial.Chebyshev.value:
                return cheb2poly(self(x).coef)
