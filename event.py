import re

import customtkinter
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.metrics import mean_squared_error as mse

from app_state import AppState
from solution import main_solution
from tools.config import LOC_TRANS, OPT_TRANS, POL_TRANS, THEME_TRANS
from utils import convert_polynomials

CURRENT_PRED = {}


INPUT_PATH = None
OUTPUT_PATH = None
LATEX = False

CURRENT_INPUT = None

PATH_LIGHT = 'image/image_light.png'
PATH_DARK = 'image/image_dark.png'
APP = None

# Plotting
X_DATA = [0]
Y_DATA_TRUE = [0]
Y_DATA_PRED = [0]

N = 3
M = 4

POLYNOMS_NAMES = {"Ерміта": 'H',
                  "Лежандра": 'L',
                  "Лаґерра": 'L',
                  "Чебишова": 'T', }



NORMALIZED = {True: 'з нормуванням',
              False: 'у відновленій формі'}


def init_app_event(my_app):
    global APP
    APP = my_app

# Options


def toggle_render():
    global LATEX
    if APP.y_selector.render_var.get() == "on":
        LATEX = True
    else:
        LATEX = False


def change_func(y: str):
    global CURRENT_PRED
    # y_pred = CURRENT_PRED[y]
    APP.y_selector.cur_y.set(y)
    make_plots()


def change_polynom(new_pol: str):
    AppState.pol = POL_TRANS[new_pol].value


def change_method(new_opt: str):
    AppState.opt = OPT_TRANS[new_opt].value


def calculate_y():
    global X_DATA, Y_DATA_TRUE, Y_DATA_PRED
    update_y_selector()

    way = APP.mist_view.approach_radio_var.get()
    x1_deg = int(APP.polynom_view.X1_deg.get())
    x2_deg = int(APP.polynom_view.X2_deg.get())
    x3_deg = int(APP.polynom_view.X3_deg.get())

    if way and CURRENT_METHOD in ["Псевдооберненої матриці",
                                  "Генетичний алгоритм"]:
        total = 'Для мультиплікативної форми залежностей необхідно обрати градієнтний метод вирішення несумісної системи'
        APP.main_tabview.results_textbox.delete('1.0', customtkinter.END)
        APP.main_tabview.results_textbox.insert('0.0', total)
    else:
        x, y = format_input()
        X_DATA = x
        Y_DATA_TRUE = y
        res_y, res_lam, res_a, res_c = main_solution(x, y, method=CURRENT_METHOD, polynom=CURRENT_POLYNOM, degs=(x1_deg, x2_deg, x3_deg))
        Y_DATA_PRED = res_y
        make_plots()
        total = ''
        if not way: 
            total += str_c_coeffs(res_c)
            total += str_a_coeffs(res_a)
        total += str_lam_coeffs(res_lam, pol=CURRENT_POLYNOM, mul=way)
        if not way:
            total += str_lam_pol_coeffs(res_lam, pol=CURRENT_POLYNOM)
        APP.main_tabview.results_textbox.delete('1.0', customtkinter.END)
        APP.main_tabview.results_textbox.insert('0.0', total)

# Appearance


def change_theme(new_theme: str):
    AppState.theme = THEME_TRANS[new_theme].value
    customtkinter.set_appearance_mode(AppState.theme)


def change_locale(new_loc: str):
    AppState.lang = LOC_TRANS[new_loc].value
    APP.update_locale()


def update_y_selector():
    APP.y_selector.cur_y.set('Y1')
    y_dim = int(APP.vector_view.Y_dim.get())
    y_values = [f'Y{i}' for i in range(1, y_dim + 1)]
    APP.y_selector.plot_y_function_optionmenu.configure(values=y_values)


def make_plots(key=1):
    if key == 1:
        cur_y = int(APP.y_selector.cur_y.get()[1:])
        y_true = Y_DATA_TRUE[cur_y - 1]
        y_pred = Y_DATA_PRED[cur_y - 1]
    else:
        y_true = Y_DATA_TRUE
        y_pred = Y_DATA_PRED
    with plt.style.context('default'):
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(1, len(y_true) + 1), y_true,
                label='Значення вибірки')
        ax.plot(range(1, len(y_pred) + 1), y_pred,
                label='Апроксимовані значення')
        ax.set_title(f'MSE {mse(y_true, y_pred):.3f}', y=1.04)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                  ncol=2, fancybox=True, shadow=True)
        fig.savefig(PATH_LIGHT)

    with plt.style.context('dark_background'):
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(1, len(y_true) + 1), y_true,
                label='Значення вибірки')
        ax.plot(range(1, len(y_pred) + 1), y_pred,
                label='Апроксимовані значення')
        ax.set_title(f'MSE {mse(y_true, y_pred):.3f}', y=1.04)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                  ncol=2, fancybox=True, shadow=True)
        fig.savefig(PATH_DARK)

    if key == 1:
        my_image = customtkinter.CTkImage(light_image=Image.open(PATH_LIGHT),
                                          dark_image=Image.open(PATH_DARK),
                                          size=(520, 450))
        APP.main_tabview.results_plot.configure(image=my_image)
        APP.main_tabview.results_plot.pack(
            side="bottom", fill="both", expand="yes")


# printing results

def str_c_coeffs(c):
    global LATEX
    total = f'Матриця коефіцієнтів C\n\n'
    if not LATEX:
        for ind, coef in enumerate(c):
            res = f'Ф{ind + 1}(' + \
                ', '.join([f'x{h}' for h in range(1, N)]) + f', x{N}) ='
            for vec_id, val in enumerate(coef):
                res += f'{val.numpy()[0]:.4f}*Ф{ind + 1}{vec_id+ 1 }(x{vec_id + 1}) '
            res = re.sub(r'( )(\d)', r'\1+ \2', res, count=len(res.split(' ')))
            res = res.replace('=', '= ').replace('-', '- ').rstrip()
            total += res + '\n'
    else:
        for ind, coef in enumerate(c):
            res = f'\Phi_{{{ind + 1}}}(' + ', '.join(
                [f'x_{{{h}}}' for h in range(1, N)]) + f', x_{{{N}}}) ='
            for vec_id, val in enumerate(coef):
                res += f'{val.numpy()[0]:.4f} \cdot Ф_{{{ind + 1}{vec_id + 1}}}(x_{{{vec_id + 1}}}) '
            res = re.sub(r'( )(\d)', r'\1+ \2', res, count=len(res.split(' ')))
            res = res.replace('=', '= ').replace('-', '- ').rstrip()
            total += res + '\n'
    return total + '\n'


def str_a_coeffs(a):
    global LATEX
    total = f'Матриця коефіцієнтів A\n\n'
    if not LATEX:
        for ind, coef in enumerate(a):
            for vec_id, x_vec in enumerate(coef):
                res = f'Ф{ind + 1}{vec_id + 1}(x{vec_id + 1}) ='
                for elem_id, val in enumerate(x_vec.numpy()):
                    res += f'{val:.4f}*Ψ{vec_id + 1}{elem_id + 1}(x{vec_id + 1}{elem_id + 1}) '
                res = re.sub(r'( )(\d)', r'\1+ \2', res,
                             count=len(res.split(' ')))
                res = res.replace('=', '= ').replace('-', '- ').rstrip()
                total += res + '\n'
            total += '\n'
    else:
        for ind, coef in enumerate(a):
            for vec_id, x_vec in enumerate(coef):
                res = f'\Phi_{{{ind + 1}{vec_id + 1}}}(x_{{{vec_id + 1}}}) ='
                for elem_id, val in enumerate(x_vec.numpy()):
                    res += f'{val:.4f} \cdot \Psi_{{{vec_id + 1}{elem_id + 1}}}(x_{{{vec_id + 1}{elem_id + 1}}}) '
                res = re.sub(r'( )(\d)', r'\1+ \2', res,
                             count=len(res.split(' ')))
                res = res.replace('=', '= ').replace('-', '- ').rstrip()
                total += res + '\n'
            total += '\n'
    return total


def str_lam_coeffs(lam, pol, mul=False):
    global LATEX
    if mul:
        lam = np.array(lam) / 13
    pol_name = POLYNOMS_NAMES[pol]
    total = f'Отримані функції через поліноми {pol}\n\n'
    if mul:
        if not LATEX:
            for ind, coef in enumerate(lam):
                res = f'Ф{ind + 1}(' + \
                    ', '.join([f'x{h}' for h in range(1, N)]) + f', x{N}) ='
                for vec_id, x_vec in enumerate(coef):
                    for elem_id, x_elem in enumerate(x_vec):
                        for deg, val in enumerate(x_elem.numpy()):
                            res += f'{val:.4f}*ln({pol_name}{deg}(x{vec_id + 1}{elem_id + 1}) 1) '
                res = re.sub(r'( )(\d)', r'\1+ \2', res, count=len(res.split(' ')))
                res = res.replace('=', '= ').replace('-', '- ').rstrip()
                total += res + '\n\n'
        else:
            for ind, coef in enumerate(lam):
                res = f'\Phi_{{{ind + 1}}}(' + ', '.join(
                    [f'x_{{{h}}}' for h in range(1, N)]) + f', x_{{{N}}}) ='
                for vec_id, x_vec in enumerate(coef):
                    for elem_id, x_elem in enumerate(x_vec):
                        for deg, val in enumerate(x_elem.numpy()):
                            res += fr'{val:.4f} \cdot \ln \left ( {pol_name}_{{{deg}}}(x_{{{vec_id + 1}{elem_id + 1}}}) 1 \right ) '
                res = re.sub(r'( )(\d)', r'\1+ \2', res, count=len(res.split(' ')))
                res = res.replace('=', '= ').replace('-', '- ').rstrip()
                total += res + '\n\n'
    else:
        if not LATEX:
            for ind, coef in enumerate(lam):
                res = f'Ф{ind + 1}(' + \
                    ', '.join([f'x{h}' for h in range(1, N)]) + f', x{N}) ='
                for vec_id, x_vec in enumerate(coef):
                    for elem_id, x_elem in enumerate(x_vec):
                        for deg, val in enumerate(x_elem.numpy()):
                            res += f'{val:.4f}*{pol_name}{deg}(x{vec_id + 1}{elem_id + 1}) '
                res = re.sub(r'( )(\d)', r'\1+ \2', res, count=len(res.split(' ')))
                res = res.replace('=', '= ').replace('-', '- ').rstrip()
                total += res + '\n\n'
        else:
            for ind, coef in enumerate(lam):
                res = f'\Phi_{{{ind + 1}}}(' + ', '.join(
                    [f'x_{{{h}}}' for h in range(1, N)]) + f', x_{{{N}}}) ='
                for vec_id, x_vec in enumerate(coef):
                    for elem_id, x_elem in enumerate(x_vec):
                        for deg, val in enumerate(x_elem.numpy()):
                            res += f'{val:.4f} \cdot {pol_name}_{{{deg}}}(x_{{{vec_id + 1}{elem_id + 1}}}) '
                res = re.sub(r'( )(\d)', r'\1+ \2', res, count=len(res.split(' ')))
                res = res.replace('=', '= ').replace('-', '- ').rstrip()
                total += res + '\n\n'
    return total


def str_lam_pol_coeffs(lam, pol, is_normalized=False):
    global LATEX
    total = f'Отримані функції y вигляді многочленів ({NORMALIZED[is_normalized]})\n\n'
    biases, coeffs = convert_polynomials(coeffs=lam, pol=pol)
    if not LATEX:
        for ind, coef in enumerate(coeffs):
            res = f'Ф{ind + 1}(' + ', '.join(
                [f'x{h}' for h in range(1, N)]) + f', x{N}) ={biases[ind]:.4f} '
            for vec_id, x_vec in enumerate(coef):
                for elem_id, x_elem in enumerate(x_vec):
                    for deg, val in enumerate(x_elem):
                        res += f'{val:.4f}*x{vec_id+1}{elem_id + 1}^{deg + 1} '
            res = re.sub(r'( )(\d)', r'\1+ \2', res, count=len(res.split(' ')))
            res = res.replace('=', '= ').replace('-', '- ').rstrip()
            total += res + '\n\n'
    else:
        for ind, coef in enumerate(coeffs):
            res = f'\Phi_{{{ind + 1}}}(' + ', '.join(
                [f'x_{{{h}}}' for h in range(1, N)]) + f', x_{{{N}}}) ={biases[ind]:.4f} '
            for vec_id, x_vec in enumerate(coef):
                for elem_id, x_elem in enumerate(x_vec):
                    for deg, val in enumerate(x_elem):
                        res += f'{val:.4f} \cdot x_{{{vec_id + 1}{elem_id + 1}}}^{{{deg + 1}}} '
            res = re.sub(r'( )(\d)', r'\1+ \2', res, count=len(res.split(' ')))
            res = res.replace('=', '= ').replace('-', '- ').rstrip()
            total += res + '\n\n'
    return total


# Input
def manual_input():
    global CURRENT_INPUT
    dialog = customtkinter.CTkInputDialog(
        text="Введіть вибірку:", title="Введення даних")
    data = dialog.get_input()
    if data is not None and data.replace(' ', '') != '':
        CURRENT_INPUT = data


def input_file():
    global INPUT_PATH, CURRENT_INPUT
    filename = customtkinter.filedialog.askopenfilename()
    INPUT_PATH = filename
    with open(filename, 'r') as file:
        CURRENT_INPUT = file.read()

    update_path(filename)


def output_file():
    global OUTPUT_PATH
    filename = customtkinter.filedialog.askopenfilename()
    OUTPUT_PATH = filename
    update_path(filename, key=2)


def update_path(path, key=1):
    if key == 1:
        APP.input_view.entry_file_input.delete(0, 'end')
        APP.input_view.entry_file_input.insert(0, path)
    else:
        APP.input_view.entry_file_output.delete(0, 'end')
        APP.input_view.entry_file_output.insert(0, path)


def format_input():
    if CURRENT_INPUT is None:
        return

    x = {}
    y = {}
    x1_dim = APP.vector_view.X1_dim.get()
    x2_dim = APP.vector_view.X2_dim.get()
    x3_dim = APP.vector_view.X3_dim.get()
    y_dim = APP.vector_view.Y_dim.get()

    for block in CURRENT_INPUT.split('\n\n'):
        if block != '':
            block = block.replace(' ', '').replace('\t', '').strip('\n')
            if block[0] in ['X', 'x', 'Х', 'х']:
                if block[2:].split('\n')[0] == '1':
                    x[int(block[1])] = {}

                x[int(block[1])][int(block[2:].split('\n')[0])] = [
                    float(i.replace(',', '.').strip(' ').strip('\n'))for i in block.split('\n')[1:]]

            if block[0] in ['Y', 'y', 'У', 'у']:
                y[int(block[1:1 + len(y_dim)])] = [float(i.replace(',',
                                                                   '.').strip(' ').strip('\n')) for i in block.split('\n')[1:]]

    res_x = [[x[key_1][key_2]
              for key_2 in sorted(x[key_1])] for key_1 in sorted(x)]
    res_y = [y[key] for key in sorted(y)]

    assert len(res_y) == int(y_dim)
    assert len(res_x) == 3
    assert len(res_x[0]) == int(x1_dim)
    assert len(res_x[1]) == int(x2_dim)
    assert len(res_x[2]) == int(x3_dim)

    return res_x, res_y
