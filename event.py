import customtkinter
import matplotlib.pyplot as plt
from PIL import Image
from solution import main_solution

CURRENT_THEME = None
CURRENT_POLYNOM = "Ерміта"
CURRENT_METHOD = "Adam"
CURRENT_PRED = {}

WEIGHTS =  ["Середнє", "MaxMin"]

INPUT_PATH = None
OUTPUT_PATH = None

CURRENT_INPUT = None

PATH_LIGHT = 'image/image_light.png'
PATH_DARK = 'image/image_dark.png'
APP = None

#Plotting
X_DATA = [0]
Y_DATA_TRUE = [0]
Y_DATA_PRED = [0]


def init_app_event(my_app):
    global APP
    APP = my_app

# Options
def change_polynom(polynom: str):
    global CURRENT_POLYNOM
    CURRENT_POLYNOM = polynom


def change_method(method: str):
    global CURRENT_METHOD
    CURRENT_METHOD = method


def calculate_y():
    global X_DATA, Y_DATA_TRUE, Y_DATA_PRED
    update_y_selector()

    weights = WEIGHTS[APP.additional_view.weights_radio_var.get()]
    x1_deg = int(APP.polynom_view.X1_deg.get())
    x2_deg = int(APP.polynom_view.X2_deg.get())
    x3_deg = int(APP.polynom_view.X3_deg.get())

    x, y = format_input()
    X_DATA = x
    Y_DATA_TRUE = y
    res_y = main_solution(x, y, method=CURRENT_METHOD, polynom=CURRENT_POLYNOM, \
                          weights=weights, degs=(x1_deg, x2_deg, x3_deg))
    Y_DATA_PRED = res_y
    make_plots()

# Appearance
def change_appearance_mode_event(new_appearance_mode: str):
    global CURRENT_THEME
    trans = {"Світла": "Light",
                "Темна": "Dark"}
    customtkinter.set_appearance_mode(trans[new_appearance_mode])
    CURRENT_THEME = trans[new_appearance_mode]


def update_y_selector():
    APP.y_selector.cur_y.set('Y1')
    y_dim = int(APP.vector_view.Y_dim.get())
    y_values = [f'Y{i}' for i in range(1, y_dim + 1)]
    APP.y_selector.plot_y_function_optionmenu.configure(values=y_values)


def make_plots(key=1):
    if key==1:
        cur_y = int(APP.y_selector.cur_y.get()[1:])
        y_true = Y_DATA_TRUE[cur_y - 1]
        y_pred = Y_DATA_PRED[cur_y - 1]
    else:
        y_true = Y_DATA_TRUE
        y_pred = Y_DATA_PRED
    with plt.style.context('default'):
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(1, len(y_true) + 1), y_true, label='Значення вибірки')
        ax.plot(range(1, len(y_pred) + 1), y_pred, label='Апроксимовані значення')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                    ncol=2, fancybox=True, shadow=True)
        fig.savefig(PATH_LIGHT)

    with plt.style.context('dark_background'):
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(1, len(y_true) + 1), y_true, label='Значення вибірки')
        ax.plot(range(1, len(y_pred) + 1), y_pred, label='Апроксимовані значення')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                    ncol=2, fancybox=True, shadow=True)
        fig.savefig(PATH_DARK)

    if key == 1:
        my_image = customtkinter.CTkImage(light_image=Image.open(PATH_LIGHT),
                                dark_image=Image.open(PATH_DARK),
                                size=(520, 450))
        APP.main_tabview.results_plot.configure(image=my_image)
        APP.main_tabview.results_plot.pack(side ="bottom", fill="both", expand="yes")


def change_func(y: str):
    global CURRENT_PRED
    #y_pred = CURRENT_PRED[y]
    APP.y_selector.cur_y.set(y)
    make_plots()
    
    #master.results_plot = customtkinter.CTkLabel(master.tabview.tab("Графік"), text='', image=my_image)
    #master.results_plot.pack()

# Input 
def manual_input():
    global CURRENT_INPUT
    dialog = customtkinter.CTkInputDialog(text="Введіть вибірку:", title="Введення даних")
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
    OUTPUT_PATH =filename
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

                x[int(block[1])][int(block[2:].split('\n')[0])] = [float(i.replace(',', '.').strip(' ').strip('\n') )for i in block.split('\n')[1:]]

            if block[0] in ['Y', 'y', 'У', 'у']:
                y[int(block[1:1 + len(y_dim)])] = [float(i.replace(',', '.').strip(' ').strip('\n') ) for i in block.split('\n')[1:]]


    res_x = [[x[key_1][key_2] for key_2 in sorted(x[key_1])] for key_1 in sorted(x)]
    res_y = [y[key] for key in sorted(y)]

    assert len(res_y) == int(y_dim)
    assert len(res_x) == 3
    assert len(res_x[0]) == int(x1_dim)
    assert len(res_x[1]) == int(x2_dim)
    assert len(res_x[2]) == int(x3_dim)

    return res_x, res_y


