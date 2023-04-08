import customtkinter
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image

CURRENT_THEME = None
CURRENT_POLYNOM = "Ерміта"
CURRENT_METHOD = "Псевдооберненої матриці"
CURRENT_PRED = {}

WEIGHTS =  ["Середнє", "MaxMin"]

INPUT_PATH = None
OUTPUT_PATH = None

PATH_LIGHT = 'image_light.png'
PATH_DARK = 'image_dark.png'
APP = None

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
    cur_y = APP.y_selector.cur_y.get()
    update_y_selector()

    weights = WEIGHTS[APP.additional_view.weights_radio_var.get()]
    x1_deg = int(APP.polynom_view.X1_deg.get())
    x2_deg = int(APP.polynom_view.X2_deg.get())
    x3_deg = int(APP.polynom_view.X3_deg.get())

    x1_dim = int(APP.vector_view.X1_dim.get())
    x2_dim = int(APP.vector_view.X2_dim.get())
    x3_dim = int(APP.vector_view.X3_dim.get())
    y_dim = int(APP.vector_view.Y_dim.get())

    print(cur_y)
    print(CURRENT_METHOD)
    print(CURRENT_POLYNOM)
    print(weights)
    print(x1_deg, x2_deg, x3_deg)
    print(x1_dim, x2_dim, x3_dim, y_dim)

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
    # USE PREDICT and Y
    X_data = [] #np.arange(1, 50 + 1)
    y_data = [] #np.random.uniform(low=0, high=0.65, size=50)
    y_data_2 = [] #y_data + np.random.randn(50) * 0.1
    with plt.style.context('default'):
        fig, ax = plt.subplots(1, 1)
        ax.plot(X_data, y_data, label='Значення вибірки')
        ax.plot(X_data, y_data_2, label='Апроксимовані значення')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                    ncol=2, fancybox=True, shadow=True)
        fig.savefig(PATH_LIGHT)

    with plt.style.context('dark_background'):
        fig, ax = plt.subplots(1, 1)
        ax.plot(X_data, y_data, label='Значення вибірки')
        ax.plot(X_data, y_data_2, label='Апроксимовані значення')
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
    dialog = customtkinter.CTkInputDialog(text="Введіть вибірку:", title="Введення даних")
    print("Ручний ввід:", dialog.get_input())

def input_file():
    global INPUT_PATH
    filename = customtkinter.filedialog.askopenfilename()
    INPUT_PATH = filename
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