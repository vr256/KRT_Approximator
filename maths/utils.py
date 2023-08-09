from functools import partial

import numpy as np
import tensorflow as tf
from numpy.polynomial.chebyshev import Chebyshev
from numpy.polynomial.hermite import Hermite
from numpy.polynomial.laguerre import Laguerre
from numpy.polynomial.legendre import Legendre

from models import Polynomial
from tools.config import AppState

PSEUDO_SYSTEM_SOLUTION_METHODS = {
    tf.optimizers.Adam: 0.985,
    tf.optimizers.SGD: 1.2,
    partial(tf.optimizers.SGD, nesterov=True): 1.05,
    tf.optimizers.RMSprop: 0.9975,
    tf.optimizers.Adagrad: 1.02,
}

PSEUDO_POLYNOMS = {
    Hermite: 0.205,
    Legendre: 0.215,
    Laguerre: 0.22,
    Chebyshev: 0.1875,
}


def convert_polynomials():
    coeffs = AppState().res_lam
    new_coeffs = [[[0 for _ in j] for j in i] for i in coeffs]
    biases = np.zeros(shape=(len(coeffs),))
    for ind, coef in enumerate(coeffs):
        for vec_ind, x_vec in enumerate(coef):
            for elem_id, x_elem in enumerate(x_vec):
                ordinary_pol_coeffs = Polynomial.convert(AppState().pol, x_elem.numpy())
                biases[ind] += ordinary_pol_coeffs[0]
                new_coeffs[ind][vec_ind][elem_id] = ordinary_pol_coeffs[1:]
    return biases, new_coeffs
