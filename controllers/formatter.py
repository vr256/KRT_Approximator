import json
import os
import re

import numpy as np

from maths.utils import convert_polynomials
from models import Polynomial
from tools.config import AppState
from tools.utils import load_locale

current_module = os.path.splitext(os.path.basename(__file__))[0]


def format_txt_input():
    with open(AppState().input_file, "r", encoding="utf-8") as file:
        cur_input = file.read()
    x = {}
    y = {}
    y_dim = AppState().dims[0]
    x_dims = AppState().dims[1:]
    try:
        for block in cur_input.split("\n\n"):
            if block != "" and block != "\n":
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
        assert len(res_y) == AppState().num_y
        assert len(res_x) == AppState().num_x
        for i in range(len(res_x)):
            assert len(res_x[i]) == x_dims[i]

        return np.array(res_x), np.array(res_y)
    except AssertionError:
        return -1, -1


# TODO change name (include hierarchical level), e.g. `print`
def str_c_coeffs():
    loc = load_locale(current_module)
    rendered_res = [loc["coef_matrix"] + " C:\n\n"] * 2
    for r_ind, render in enumerate((loc["text"], loc["latex"])):
        for ind, coef in enumerate(AppState().res_c):
            res = (
                f"{render['phi']}{ind + 1}{render['end']}("
                + ", ".join(
                    [
                        f"{render['x']}{h}{render['end']}"
                        for h in range(1, AppState().num_x)
                    ],
                )
                + f", {render['x']}{AppState().num_x}{render['end']}) ="
            )
            for vec_id, val in enumerate(coef):
                res += (
                    f"{val.numpy()[0]:.4f}{render['mul']}"
                    + f"{render['phi']}{ind + 1}{vec_id + 1}{render['end']}"
                    + f"({render['x']}{vec_id + 1}{render['end']}) "
                )
            res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
            res = res.replace("=", "= ").replace("-", "- ").rstrip()
            rendered_res[r_ind] += res + "\n\n"

    return [i + "\n" for i in rendered_res]


def str_a_coeffs():
    loc = load_locale(current_module)
    total = loc["coef_matrix"] + " A:\n\n"
    plain_text, latex = "", ""

    for ind, coef in enumerate(AppState().res_a):
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

    for ind, coef in enumerate(AppState().res_a):
        for vec_id, x_vec in enumerate(coef):
            res = f"\Phi_{{{ind + 1}{vec_id + 1}}}(x_{{{vec_id + 1}}}) ="
            for elem_id, val in enumerate(x_vec.numpy()):
                res += f"{val:.4f} \cdot \Psi_{{{vec_id + 1}{elem_id + 1}}}(x_{{{vec_id + 1}{elem_id + 1}}}) "
            res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
            res = res.replace("=", "= ").replace("-", "- ").rstrip()
            total += res + "\n"
        latex += "\n"

    return total + plain_text + "\n", total + latex + "\n"


def str_lam_coeffs():
    lam = AppState().res_lam
    loc = load_locale(current_module)
    with open(AppState().lang, "r", encoding="utf-8") as file:
        polynomials = json.load(file)["config_view"]["polynomials"]

    pol_alias = Polynomial.alias_repr(AppState().pol)
    pol_name = polynomials[list(Polynomial).index(Polynomial(AppState().pol))]
    total = loc["ort_pol_message"] + f" {pol_name}" + loc["possesive_case"] + ":\n\n"
    plain_text, latex = "", ""

    for ind, coef in enumerate(lam):
        res = (
            f"Ф{ind + 1}("
            + ", ".join([f"x{h}" for h in range(1, AppState().num_x)])
            + f", x{AppState().num_x}) ="
        )
        for vec_id, x_vec in enumerate(coef):
            for elem_id, x_elem in enumerate(x_vec):
                for deg, val in enumerate(x_elem.numpy()):
                    res += f"{val:.4f}*{pol_alias}{deg}(x{vec_id + 1}{elem_id + 1}) "
        res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
        res = res.replace("=", "= ").replace("-", "- ").rstrip()
        plain_text += res + "\n\n"

    for ind, coef in enumerate(lam):
        res = (
            f"\Phi_{{{ind + 1}}}("
            + ", ".join([f"x_{{{h}}}" for h in range(1, AppState().num_x)])
            + f", x_{{{AppState().num_x}}}) ="
        )
        for vec_id, x_vec in enumerate(coef):
            for elem_id, x_elem in enumerate(x_vec):
                for deg, val in enumerate(x_elem.numpy()):
                    res += f"{val:.4f} \cdot {pol_alias}_{{{deg}}}(x_{{{vec_id + 1}{elem_id + 1}}}) "
        res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
        res = res.replace("=", "= ").replace("-", "- ").rstrip()
        latex += res + "\n\n"

    return total + plain_text + "\n", total + latex + "\n"


def str_lam_pol_coeffs():
    loc = load_locale(current_module)
    total = loc["conv_pol_message"] + ":\n\n"
    biases, coeffs = convert_polynomials()
    plain_text, latex = "", ""

    for ind, coef in enumerate(coeffs):
        res = (
            f"Ф{ind + 1}("
            + ", ".join([f"x{h}" for h in range(1, AppState().num_x)])
            + f", x{AppState().num_x}) ={biases[ind]:.4f} "
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
            + ", ".join([f"x_{{{h}}}" for h in range(1, AppState().num_x)])
            + f", x_{{{AppState().num_x}}}) ={biases[ind]:.4f} "
        )
        for vec_id, x_vec in enumerate(coef):
            for elem_id, x_elem in enumerate(x_vec):
                for deg, val in enumerate(x_elem):
                    res += f"{val:.4f} \cdot x_{{{vec_id + 1}{elem_id + 1}}}^{{{deg + 1}}} "
        res = re.sub(r"( )(\d)", r"\1+ \2", res, count=len(res.split(" ")))
        res = res.replace("=", "= ").replace("-", "- ").rstrip()
        latex += res + "\n\n"

    return total + plain_text + "\n", total + latex + "\n"


def get_text_results():
    if hasattr(AppState(), "res_lam"):
        res = tuple(  # TODO revise order
            zip(str_lam_coeffs(), str_lam_pol_coeffs(), str_c_coeffs(), str_a_coeffs()),
        )
        return ["".join(i) for i in res]
    else:
        return "", ""
