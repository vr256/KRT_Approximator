import re

import numpy as np

from maths.utils import convert_polynomials
from models.model import Polynomial
from tools.config import AppState

# Plotting
# TODO arbitrary N and M
N = 3
M = 4

NORMALIZED = {True: "з нормуванням", False: "у відновленій формі"}


def format_input(cur_input: str):
    x = {}
    y = {}
    y_dim, x1_dim, x2_dim, x3_dim = AppState.dims

    for block in cur_input.split("\n\n"):
        if block != "":
            block = block.replace(" ", "").replace("\t", "").strip("\n")
            if block[0] in ["X", "x", "Х", "х"]:
                if block[2:].split("\n")[0] == "1":
                    x[int(block[1])] = {}

                x[int(block[1])][int(block[2:].split("\n")[0])] = [
                    float(i.replace(",", ".").strip(" ").strip("\n"))
                    for i in block.split("\n")[1:]
                ]

            if block[0] in ["Y", "y", "У", "у"]:
                y[int(block[1 : 1 + len(str(y_dim))])] = [
                    float(i.replace(",", ".").strip(" ").strip("\n"))
                    for i in block.split("\n")[1:]
                ]

    res_x = [[x[key_1][key_2] for key_2 in sorted(x[key_1])] for key_1 in sorted(x)]
    res_y = [y[key] for key in sorted(y)]
    assert len(res_y) == y_dim
    assert len(res_x) == 3
    assert len(res_x[0]) == x1_dim
    assert len(res_x[1]) == x2_dim
    assert len(res_x[2]) == x3_dim

    return np.array(res_x), np.array(res_y)


# printing results


def str_c_coeffs(c):
    total = f"Матриця коефіцієнтів C\n\n"
    plain_text, latex = "", ""

    for ind, coef in enumerate(c):
        res = f"Ф{ind + 1}(" + ", ".join([f"x{h}" for h in range(1, N)]) + f", x{N}) ="
        for vec_id, val in enumerate(coef):
            res += f"{val.numpy()[0]:.4f}*Ф{ind + 1}{vec_id+ 1 }(x{vec_id + 1}) "
        res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
        res = res.replace("=", "= ").replace("-", "- ").rstrip()
        plain_text += res + "\n"

    for ind, coef in enumerate(c):
        res = (
            f"\Phi_{{{ind + 1}}}("
            + ", ".join([f"x_{{{h}}}" for h in range(1, N)])
            + f", x_{{{N}}}) ="
        )
        for vec_id, val in enumerate(coef):
            res += f"{val.numpy()[0]:.4f} \cdot Ф_{{{ind + 1}{vec_id + 1}}}(x_{{{vec_id + 1}}}) "
        res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
        res = res.replace("=", "= ").replace("-", "- ").rstrip()
        latex += res + "\n"

    return total + plain_text + "\n", total + latex + "\n"


def str_a_coeffs(a):
    total = f"Матриця коефіцієнтів A\n\n"
    plain_text, latex = "", ""

    for ind, coef in enumerate(a):
        for vec_id, x_vec in enumerate(coef):
            res = f"Ф{ind + 1}{vec_id + 1}(x{vec_id + 1}) ="
            for elem_id, val in enumerate(x_vec.numpy()):
                res += (
                    f"{val:.4f}*Ψ{vec_id + 1}{elem_id + 1}(x{vec_id + 1}{elem_id + 1}) "
                )
            res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
            res = res.replace("=", "= ").replace("-", "- ").rstrip()
            total += res + "\n"
        plain_text += "\n"

    for ind, coef in enumerate(a):
        for vec_id, x_vec in enumerate(coef):
            res = f"\Phi_{{{ind + 1}{vec_id + 1}}}(x_{{{vec_id + 1}}}) ="
            for elem_id, val in enumerate(x_vec.numpy()):
                res += f"{val:.4f} \cdot \Psi_{{{vec_id + 1}{elem_id + 1}}}(x_{{{vec_id + 1}{elem_id + 1}}}) "
            res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
            res = res.replace("=", "= ").replace("-", "- ").rstrip()
            total += res + "\n"
        latex += "\n"

    return total + plain_text, total + latex


def str_lam_coeffs(lam, pol):
    pol_name = Polynomial.alias_repr(pol)
    total = f"Отримані функції через поліноми {pol}\n\n"
    plain_text, latex = "", ""

    for ind, coef in enumerate(lam):
        res = f"Ф{ind + 1}(" + ", ".join([f"x{h}" for h in range(1, N)]) + f", x{N}) ="
        for vec_id, x_vec in enumerate(coef):
            for elem_id, x_elem in enumerate(x_vec):
                for deg, val in enumerate(x_elem.numpy()):
                    res += f"{val:.4f}*{pol_name}{deg}(x{vec_id + 1}{elem_id + 1}) "
        res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
        res = res.replace("=", "= ").replace("-", "- ").rstrip()
        plain_text += res + "\n\n"

    for ind, coef in enumerate(lam):
        res = (
            f"\Phi_{{{ind + 1}}}("
            + ", ".join([f"x_{{{h}}}" for h in range(1, N)])
            + f", x_{{{N}}}) ="
        )
        for vec_id, x_vec in enumerate(coef):
            for elem_id, x_elem in enumerate(x_vec):
                for deg, val in enumerate(x_elem.numpy()):
                    res += f"{val:.4f} \cdot {pol_name}_{{{deg}}}(x_{{{vec_id + 1}{elem_id + 1}}}) "
        res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
        res = res.replace("=", "= ").replace("-", "- ").rstrip()
        latex += res + "\n\n"

    return total + plain_text, total + latex


def str_lam_pol_coeffs(lam, pol, is_normalized=False):
    total = f"Отримані функції y вигляді многочленів ({NORMALIZED[is_normalized]})\n\n"
    biases, coeffs = convert_polynomials(coeffs=lam, pol=pol)
    plain_text, latex = "", ""

    for ind, coef in enumerate(coeffs):
        res = (
            f"Ф{ind + 1}("
            + ", ".join([f"x{h}" for h in range(1, N)])
            + f", x{N}) ={biases[ind]:.4f} "
        )
        for vec_id, x_vec in enumerate(coef):
            for elem_id, x_elem in enumerate(x_vec):
                for deg, val in enumerate(x_elem):
                    res += f"{val:.4f}*x{vec_id+1}{elem_id + 1}^{deg + 1} "
        res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
        res = res.replace("=", "= ").replace("-", "- ").rstrip()
        plain_text += res + "\n\n"

    for ind, coef in enumerate(coeffs):
        res = (
            f"\Phi_{{{ind + 1}}}("
            + ", ".join([f"x_{{{h}}}" for h in range(1, N)])
            + f", x_{{{N}}}) ={biases[ind]:.4f} "
        )
        for vec_id, x_vec in enumerate(coef):
            for elem_id, x_elem in enumerate(x_vec):
                for deg, val in enumerate(x_elem):
                    res += f"{val:.4f} \cdot x_{{{vec_id + 1}{elem_id + 1}}}^{{{deg + 1}}} "
        res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
        res = res.replace("=", "= ").replace("-", "- ").rstrip()
        latex += res + "\n\n"

    return total + plain_text, total + latex
