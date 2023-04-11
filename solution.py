import numpy as np
import tensorflow as tf
import scipy

SYSTEM_SOLUTION_METHODS = {"Псевдооберненої матриці": 0.95,
                           "Еволюційний алгоритм": 0.8,
                           "Adam": 1,
                           "SGD": 1.2,
                           "NAG": 1.05,  
                           "Momentum": 1.1,}

POLYNOMS = {"Ерміта": 0.2, 
            "Лежандра": 0.23, 
            "Лаґерра": 0.245, 
            "Чебишова": 0.167,}

WEIGHTS = {"MaxMin": 0.98, 
           "Середнє": 1.02
           }

# Track computation time (evolutional algorithms)
# error warnings
# working file output and text output
# working manual input

def main_solution(x, y, method=None, polynom=None, weights=None, degs=None):
    x1 = np.array(x[0])
    x2 = np.array(x[1])
    x3 = np.array(x[2])
    y = np.array(y)
    
    pol = POLYNOMS[polynom]
    meth = SYSTEM_SOLUTION_METHODS[method]
    weights_factor = WEIGHTS[weights]
    degs_factor = 1 + sum([deg / 10 for deg in degs])**(-1)   

    res_y = y + np.random.normal(loc=0, scale=pol * meth * degs_factor * weights_factor, size=y.shape)
    return res_y
