import numpy as np
from numpy.polynomial.chebyshev import Chebyshev, cheb2poly
from numpy.polynomial.hermite import Hermite, herm2poly
from numpy.polynomial.laguerre import Laguerre, lag2poly
from numpy.polynomial.legendre import Legendre, leg2poly

POLYNOMS = {"Ерміта": (Hermite, herm2poly),
            "Лежандра": (Legendre, leg2poly),
            "Лаґерра": (Laguerre, lag2poly), 
            "Чебишова": (Chebyshev, cheb2poly)}

PSEUDO_SYSTEM_SOLUTION_METHODS = {"Псевдооберненої матриці": 0.115,
                           "Генетичний алгоритм": 0.875,
                           "Adam": 0.985,
                           "SGD": 1.2,
                           "Nesterov": 1.05,  
                           "RMSprop": 0.9975,
                           "Adagrad": 1.02, 
                           }

PSEUDO_POLYNOMS = {"Ерміта": 0.205, 
            "Лежандра": 0.215, 
            "Лаґерра": 0.22, 
            "Чебишова": 0.1875,
            }

PSEUDO_WEIGHTS = {"MaxMin": 0.98, 
           "Середнє": 1.02
           }

def convert_polynomials(coeffs, pol):
    new_coeffs = [[[0 for _ in j] for j in i] for i in coeffs]
    biases = np.zeros(shape=(len(coeffs), ))
    pol_type = POLYNOMS[pol][0]
    converter = POLYNOMS[pol][1]
    for ind, coef in enumerate(coeffs):
        for vec_ind, x_vec in enumerate(coef):
            for elem_id, x_elem in enumerate(x_vec):
                simple_pol_coeffs = converter(pol_type(x_elem.numpy()).coef)
                biases[ind] += simple_pol_coeffs[0]
                new_coeffs[ind][vec_ind][elem_id] = simple_pol_coeffs[1:]
    return biases, new_coeffs