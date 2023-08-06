import json
import os
import sys
import tkinter

import customtkinter
from PIL import Image

from app import AppState
from event import (
    calculate_y,
    change_appearance_mode_event,
    change_func,
    make_plots,
    toggle_render,
)
from tools.config import PATH_DARK, PATH_LIGHT

filepath = os.path.splitext(os.path.basename(__file__))[0]
with open(AppState.lang.value, 'r', encoding='utf-8') as file:
    loc = json.load(file)


class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self, text=loc[filepath]['header'],
            font=customtkinter.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))
        self.info_label = customtkinter.CTkLabel(
            self, text=loc[filepath]['info'], anchor="w")
        self.info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self, text=loc[filepath]['theme_caption'], anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=loc[filepath]['themes'],
                                                                       command=change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=10, pady=(0, 10))


class YSelector(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=3, column=1, sticky="nsew", padx=(20, 0), pady=10)

        self.label_y_function_selector = customtkinter.CTkLabel(
            self, text=loc[filepath]['plot_caption'])
        self.label_y_function_selector.grid(
            row=2, column=1, padx=(20, 5), pady=5)
        self.cur_y = tkinter.StringVar(value='Y1')
        self.plot_y_function_optionmenu = customtkinter.CTkOptionMenu(self, variable=self.cur_y,
                                                                      values=['Y1', 'Y2', 'Y3', 'Y4'],
                                                                      command=change_func)
        self.plot_y_function_optionmenu.grid(row=2, column=2, padx=10, pady=5)

        self.render_label = customtkinter.CTkLabel(self,
                                                   text="Latex")
        self.render_label.grid(
            row=2, column=3, padx=(10, 5), pady=5)

        self.render_var = customtkinter.StringVar(value="off")
        self.latex_checkbox = customtkinter.CTkCheckBox(self, command=toggle_render, text="",
                                                        variable=self.render_var, onvalue="on", offvalue="off")
        self.latex_checkbox.grid(row=2, column=4, padx=5, pady=5)


class YCalculator(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=3, column=2, padx=(10, 10), pady=10, sticky="nsew")
        self.calculate_y_button = customtkinter.CTkButton(self, text="Знайти наближення",
                                                          command=calculate_y)
        self.calculate_y_button.grid(
            row=0, padx=(35, 10), pady=5, sticky="nsew")
        self.calculate_y_button.pack(side="bottom", fill="both", expand="yes")


class MainTabview(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, rowspan=2, column=1, columnspan=2,
                  padx=(5, 0), pady=(10, 0), sticky="nsew")
        self.add("Результати")
        self.add("Графік")
        self.tab("Графік").grid_columnconfigure(0, weight=1)
        self.tab("Результати").grid_columnconfigure(0, weight=1)

        # text
        self.results_textbox = customtkinter.CTkTextbox(
            self.tab("Результати"))
        self.results_textbox.grid(row=0, padx=10, pady=5, sticky="nsew")
        self.results_textbox.pack(side="bottom", fill="both", expand="yes")

        # plots
        make_plots(key=2)
        my_image = customtkinter.CTkImage(light_image=Image.open(PATH_LIGHT),
                                          dark_image=Image.open(PATH_DARK),
                                          size=(520, 450))
        self.results_plot = customtkinter.CTkLabel(
            self.tab("Графік"), text='', image=my_image)
        self.results_plot.pack(side="bottom", fill="both", expand="yes")
