import numpy as np
from sklearn.preprocessing import MinMaxScaler

from models.additive import AdditiveModel
from src.model import Polynomial
from src.tools.config import AppState

NUM_EPOCH = 10


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


def build_polynomial_matrix(X, degs, p_type):
    # TODO choose better names
    T = []
    for record in range(X[0].shape[-1]):
        T_record = []
        for j in range(len(X)):
            X_j = X[j][:, record]
            P = degs[j]
            T_j = np.zeros(shape=[P + 1, len(X_j)])
            for cur_p in range(P + 1):
                T_j[cur_p] = [p_type([0] * cur_p + [1])(x_k) for x_k in X_j]

            T_record.append(np.transpose(T_j))
        T.append(T_record)
    return T


def run(x_input, y, method=None, polynom=None, degs=None, approach=None):
    x = []
    for i in x_input:
        x.append(np.array(i))

    x_scalers = [MinMaxScaler().fit(i.T) for i in x]  # ? Redundant most likely
    y_scaler = MinMaxScaler().fit(y.T)
    x_scaled = [scaler.transform(i.T).T for scaler, i in zip(x_scalers, x)]
    y_train = y_scaler.transform(y.T)

    x_train = build_polynomial_matrix(x_scaled, degs, polynom)

    model = AdditiveModel(
        "PolynomialRegression",
        l2_reg=0.1,
        degs=degs,
        dims=AppState().dims,
    )
    model(x_train[0])  # ! huge bug
    model.compile(optimizer=method)
    model.fit(x=x_train, y=y_train, epochs=NUM_EPOCH, to_print=True)

    lam_coeffs = model.lam
    a_coeffs = model.a
    c_coeffs = model.c
    res = model.predict(x_train)

    original_res = y_scaler.inverse_transform(res).T
    return original_res, lam_coeffs, a_coeffs, c_coeffs
