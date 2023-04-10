import numpy as np
import tensorflow as tf
import scipy

SYSTEM_SOLUTION_METHODS = {"Псевдооберненої матриці": 1,
                           "Adam": 2,
                           "SGD": 3,
                           "NAG": 4,  
                           "Momentum": 5,}

POLYNOMS = {"Ерміта": 1, 
            "Лежандра": 2, 
            "Лаґерра": 3, 
            "Чебишова": 4,}


def main_solution(x, y, method=None, polynom=None, weights=None, degs=None):
    x1 = np.array(x[0])
    x2 = np.array(x[1])
    x3 = np.array(x[2])
    y = np.array(y)

    res_y = y + np.random.normal(loc=0, scale=0.2, size=y.shape)
    return res_y
