import customtkinter
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image

CURRENT_THEME = None
CURRENT_Y = None
CURRENT_PRED = {}
PATH_LIGHT = 'image_light.png'
PATH_DARK = 'image_dark.png'

def select_polynom(master, polynom: str):
    return

def calculate_y(master):
    return

def change_method(master, method: str):
    pass

def make_plots(master, key=1):
    # USE PREDICT and Y
    X_data = np.arange(1, 50 + 1)
    y_data = np.random.uniform(low=0, high=0.65, size=50)
    y_data_2 = y_data + np.random.randn(50) * 0.1
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
        master.main_tabview.results_plot.configure(image=my_image)
        master.main_tabview.results_plot.pack(side ="bottom", fill="both", expand="yes")

def change_func(master, y: str):
    global CURRENT_PRED, CURRENT_Y
    CURRENT_Y = y
    #y_pred = CURRENT_PRED[y]
    make_plots(master)
    
    #master.results_plot = customtkinter.CTkLabel(master.tabview.tab("Графік"), text='', image=my_image)
    #master.results_plot.pack()

def change_appearance_mode_event(master, new_appearance_mode: str):
    global CURRENT_THEME
    trans = {"Світла": "Light",
                "Темна": "Dark"}
    customtkinter.set_appearance_mode(trans[new_appearance_mode])
    CURRENT_THEME = trans[new_appearance_mode]
    #CURRENT_PRED, CURRENT_Y
            
    #master.results_plot = customtkinter.CTkLabel(master.tabview.tab("Графік"), text='', image=my_image)
    #master.results_plot.pack()


def open_input_dialog_event(master):
    dialog = customtkinter.CTkInputDialog(text="Введіть вибірку:", title="Введення даних")
    print("Ручний ввід:", dialog.get_input())