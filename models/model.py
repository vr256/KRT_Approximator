from enum import Enum
from functools import partial

import tensorflow as tf
from numpy.polynomial.chebyshev import Chebyshev
from numpy.polynomial.hermite import Hermite
from numpy.polynomial.laguerre import Laguerre
from numpy.polynomial.legendre import Legendre


class Locale(Enum):
    ENG = 'locales/eng.json'
    UKR = 'locales/ukr.json'

    def translate(option: str):
        match option:
            case "English" | "Англійська":
                return Locale.ENG
            case "Ukrainian" | "Українська":
                return Locale.UKR


class Theme(Enum):
    Light = 'Light'
    Dark = 'Dark'

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
