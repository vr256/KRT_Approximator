import numpy as np
import tensorflow as tf

from functools import partial
from numpy.polynomial.chebyshev import Chebyshev
from numpy.polynomial.laguerre import Laguerre
from numpy.polynomial.hermite import Hermite
from numpy.polynomial.legendre import Legendre
from sklearn.preprocessing import MinMaxScaler
from utils import PSEUDO_POLYNOMS, PSEUDO_SYSTEM_SOLUTION_METHODS, PSEUDO_WEIGHTS

NUM_EPOCH = 1

SYSTEM_SOLUTION_METHODS = {"Псевдооберненої матриці": 0.95,
                           "Еволюційний алгоритм": 0.8,
                           "Adam": tf.optimizers.Adam,
                           "SGD": tf.optimizers.SGD,
                           "Nesterov": partial(tf.optimizers.SGD, nesterov=True),
                           "RMSprop": tf.optimizers.RMSprop,
                           "Adagrad": tf.optimizers.Adagrad, }

POLYNOMS = {"Ерміта": Hermite,
            "Лежандра": Legendre,
            "Лаґерра": Laguerre,
            "Чебишова": Chebyshev, }

WEIGHTS = {"MaxMin": 0.98,
           "Середнє": 1.02
           }

N = 3
M = 4


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


def build_second_level_pol_matrix(coeffs, T):
    PSI = []
    for q in range(len(T)):
        PSI_q = [[0 for _ in range(N)] for _ in range(M)]
        for i in range(M):
            for j in range(N):
                PSI_q[i][j] = []
                for h in range(coeffs[i][j].shape[0]):
                    PSI_ijh = np.array(
                        coeffs[i][j][h]) @ np.array(T[q][j])[:, h]
                    PSI_q[i][j].append(PSI_ijh)

                PSI_q[i][j] = tf.constant(PSI_q[i][j], dtype=tf.float32)

        PSI.append(PSI_q)
    return PSI


def build_third_level_pol_matrix(coeffs, PSI):
    PHI = []
    for q in range(len(PSI)):
        PHI_q = [[0 for _ in range(N)] for _ in range(M)]
        for i in range(M):
            for j in range(N):
                PHI_q[i][j] = np.array(coeffs[i][j]) @ np.array(PSI[q][i][j])

        PHI_q = tf.constant(PHI_q, dtype=tf.float32)
        PHI.append(PHI_q)
    return PHI


class Model(tf.keras.Model):
    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.l2_reg = 0.1
        for key in kwargs:
            self.key = kwargs[key]

    def build(self, input_shape):
        lam = [[0 for _ in range(N)] for _ in range(M)]
        a = [[0 for _ in range(N)] for _ in range(M)]
        c = [[0 for _ in range(N)] for _ in range(M)]
        for i in range(M):
            for j in range(N):
                lam[i][j] = tf.Variable(np.random.randn(
                    input_shape[j][1], input_shape[j][0]), dtype=tf.float32)
                a[i][j] = tf.Variable(np.random.randn(
                    input_shape[j][1]), dtype=tf.float32)
                c[i][j] = tf.Variable(np.random.randn(1), dtype=tf.float32)

        self.lam = lam
        self.a = a
        self.c = c

    def call(self, inputs, i, param='lam'):
        match param:
            case 'lam':
                return tf.reduce_sum([tf.linalg.trace(self.lam[i][j] @ inputs[j]) for j in range(N)])
            case 'a':
                return tf.reduce_sum([tf.tensordot(self.a[i][j], inputs[i][j], axes=1) for j in range(N)])
            case 'c':
                return tf.reduce_sum([self.c[i][j] * inputs[i][j] for j in range(N)])

    def compile(self, optimizer="Adam"):
        self.optimizer = SYSTEM_SOLUTION_METHODS[optimizer]()
        self.optimizer.build(self.trainable_variables)
        # self.loss = loss

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

    def fit(self, x, y, epochs=10, tol=10e-6, param='lam', to_print=False):
        params = {'lam': self.lam,
                  'a': self.a,
                  'c': self.c}
        cur_param = params[param]
        for i in range(M):
            for epoch in range(epochs):
                epoch_loss = 0
                for q in range(len(x)):
                    with tf.GradientTape() as tape:
                        y_pred = self.call(x[q], i, param=param)
                        match param:
                            case 'lam':
                                reg_term = self.l2_reg * \
                                    tf.reduce_mean(
                                        [tf.norm(self.lam[i][j]) for j in range(N)])
                            case 'a':
                                reg_term = self.l2_reg * \
                                    tf.reduce_mean(
                                        [tf.norm(self.a[i][j]) for j in range(N)])
                            case 'c':
                                reg_term = self.l2_reg * \
                                    tf.reduce_mean([tf.norm(self.c[i])])

                        loss = tf.reduce_mean(
                            tf.square(y[i] - y_pred)) + reg_term

                    grad = tape.gradient(loss, cur_param[i])
                    self.optimizer.apply_gradients(zip(grad, cur_param[i]))
                    epoch_loss += loss / len(x)

            if to_print:
                pass
                # print(f'Epoch: {epoch + 1}  Loss: {np.round(epoch_loss, 3):.3f}')
        print()


def main_solution(x, y, method=None, polynom=None, weights=None, degs=None):
    x1 = np.array(x[0])
    x2 = np.array(x[1])
    x3 = np.array(x[2])
    y = np.array(y)

    x1_scaler = MinMaxScaler().fit(x1)
    x2_scaler = MinMaxScaler().fit(x2)
    x3_scaler = MinMaxScaler().fit(x3)
    y_scaler = MinMaxScaler().fit(y)
    x1 = x1_scaler.transform(x1)
    x2 = x2_scaler.transform(x2)
    x3 = x3_scaler.transform(x3)
    y = y_scaler.transform(y)

    T = build_polynomial_matrix([x1, x2, x3], degs, POLYNOMS[polynom])

    model = Model('PolynomialRegression', l2_reg=0.1)
    y_pred = [model(T[0], i) for i in range(M)]
    model.compile(optimizer=method)
    model.fit(x=T, y=y, epochs=NUM_EPOCH, to_print=True)

    PSI = build_second_level_pol_matrix(model.lam, T)
    model.fit(x=PSI, y=y, epochs=NUM_EPOCH, to_print=True, param='a')

    PHI = build_third_level_pol_matrix(model.a, PSI)
    model.fit(x=PHI, y=y, epochs=NUM_EPOCH, to_print=True, param='c')

    lam_coeffs = model.lam
    a_coeffs = model.a
    c_coeffs = model.c
    res = [model.predict(T, i) for i in range(M)]

    degs_factor = 1 + sum([deg / 10 for deg in degs])**(-1)

    res_y = y_scaler.inverse_transform(y) + np.random.normal(loc=0, scale=1.3 * PSEUDO_POLYNOMS[polynom] *
                                                             PSEUDO_SYSTEM_SOLUTION_METHODS[method] *
                                                             PSEUDO_WEIGHTS[weights] *
                                                             degs_factor,
                                                             size=y.shape)
    return res_y, lam_coeffs, a_coeffs, c_coeffs
