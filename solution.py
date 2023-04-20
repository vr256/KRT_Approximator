import numpy as np
import tensorflow as tf
import scipy

from functools import partial
from numpy.polynomial.chebyshev import Chebyshev
from numpy.polynomial.laguerre import Laguerre
from numpy.polynomial.hermite import Hermite
from numpy.polynomial.legendre import Legendre

from sklearn.preprocessing import MinMaxScaler


SYSTEM_SOLUTION_METHODS = {"Псевдооберненої матриці": 0.95,
                           "Еволюційний алгоритм": 0.8,
                           "Adam": tf.optimizers.Adam,
                           "SGD": tf.optimizers.SGD,
                           "Nesterov": partial(tf.optimizers.SGD, nesterov=True),  
                           "RMSprop": tf.optimizers.RMSprop,
                           "Adagrad": tf.optimizers.Adagrad,}

POLYNOMS = {"Ерміта": Hermite, 
            "Лежандра": Legendre, 
            "Лаґерра": Laguerre, 
            "Чебишова": Chebyshev,}

WEIGHTS = {"MaxMin": 0.98, 
           "Середнє": 1.02
           }

N = 3
M = 4

# Track computation time (evolutional algorithms)
# error warnings
# working file output and text output
# working manual input

# Now
# MSE
# 

def build_polynomial_matrix(X, degs, p_type):
    T = []
    assert len(X) == N
    for q in range(X[0].shape[-1]):
        T_q = []
        for j in range(len(X)):
            X_j = X[j][:, q]
            P = degs[j]
            T_j = np.zeros(shape=[P + 1, len(X_j)])
            for cur_p in range(P + 1):
                T_j[cur_p] = [p_type([0] * cur_p + [1])(x_k) for x_k in X_j]

            T_q.append(T_j)
            
        T.append(T_q)
    return T


class Model(tf.keras.Model):
    def __init__(self, name):
        super().__init__(name)

    def build(self, input_shape):
        lam = [[0 for _ in range(N)] for _ in range(M)]
        A = []
        C = []
        lam_shape = input_shape
        for i in range(M):
            assert len(lam_shape) == N
            for j in range(N):
                lam[i][j] = tf.Variable(np.random.randn(lam_shape[j][1], lam_shape[j][0]).tolist())
                
        self.lam = lam
        self.C = C
        self.A = A
    
    def call(self, inputs, i):
        return tf.reduce_sum([tf.linalg.trace(self.lam[i][j] @ inputs[j]) for j in range(N)])
    
    def compile(self, optimizer="Adam"):
        self.optimizer = SYSTEM_SOLUTION_METHODS[optimizer]()
        self.optimizer.build(self.trainable_variables)
        #self.loss = loss
    
    def predict(self, inputs, i):
        res = []
        for q in range(len(inputs)):
            res.append(self.call(inputs[q], i))
        return res
    
    def evaluate(self, x, y, i):
        mse_loss = 0
        for q in range(len(x)):
            y_pred = self.call(x[q], i)
            mse_loss += tf.reduce_mean(tf.square(y[i] - y_pred))
        return mse_loss

    def fit(self, x, y, epochs=10, tol=10e-6, to_print=False):
        for i in range(M):
            for epoch in range(epochs):
                epoch_loss = 0
                for q in range(len(x)):
                    with tf.GradientTape() as tape:
                        y_pred = self.call(x[q], i)
                        loss = tf.reduce_mean(tf.square(y[i] - y_pred)) + 0.1 * tf.reduce_mean([tf.norm(self.lam[i][j]) for j in range(N)])

                    grad = tape.gradient(loss, self.lam[i])
                    self.optimizer.apply_gradients(zip(grad, self.lam[i]))
                    epoch_loss += loss / len(x)

            if to_print:
                print(f'Epoch: {epoch + 1}  Loss: {np.round(epoch_loss, 3):3.3f}')


def main_solution(x, y, method=None, polynom=None, weights=None, degs=None):
    x1 = np.array(x[0])
    x2 = np.array(x[1])
    x3 = np.array(x[2])
    y = np.array(y)


    # Scaling to [0, 1]
    x1_scaler = MinMaxScaler().fit(x1)
    x2_scaler = MinMaxScaler().fit(x2)
    x3_scaler = MinMaxScaler().fit(x3)
    y_scaler = MinMaxScaler().fit(y)
    x1 = x1_scaler.transform(x1)
    x2 = x2_scaler.transform(x2)
    x3 = x3_scaler.transform(x3)
    y = y_scaler.transform(y)

    T = build_polynomial_matrix([x1, x2, x3], degs, POLYNOMS[polynom])

    model = Model('PolynomialRegression')
    y_pred = [model(T[0], i) for i in range(M)]
    print(y_pred)
    print(method)
    model.compile(optimizer=method)
    model.fit(x=T, y=y, epochs=20, to_print=True)
    res = [model.predict(T, i) for i in range(M)]

    pol = POLYNOMS[polynom]
    meth = SYSTEM_SOLUTION_METHODS[method]
    weights_factor = WEIGHTS[weights]
    degs_factor = 1 + sum([deg / 10 for deg in degs])**(-1)   

    res_y = y + np.random.normal(loc=0, scale=pol * meth * degs_factor * weights_factor, size=y.shape)
    return res_y
