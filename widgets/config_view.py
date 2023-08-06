import json
import os
import sys
import tkinter

import customtkinter
from PIL import Image

from app import AppState
from event import change_method, change_polynom, input_file, manual_input, output_file
from tools.config import SEARCH_ICON

filepath = os.path.splitext(os.path.basename(__file__))[0]
with open(AppState.lang.value, 'r', encoding='utf-8') as file:
    loc = json.load(file)


class Optimizer(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=3, column=3, columnspan=2,
                  sticky="nsew", padx=10, pady=10)
        self.label_system_solution_selector = customtkinter.CTkLabel(
            self, text="Оптимізатор градієнтного спуску:")
        self.label_system_solution_selector.grid(
            row=2, column=1, padx=(20, 5), pady=5)
        self.opt_system_method = customtkinter.CTkOptionMenu(self, values=loc[filepath]['optimizers'],
                                                             command=change_method)
        self.opt_system_method.grid(row=2, column=2, padx=10, pady=5)


class VectorView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._scrollbar.configure(width=0)
        self.grid(row=0, column=3, padx=(5, 5), pady=(30, 5), sticky="nsew")

        self.X1_dim = tkinter.StringVar(value='2')
        self.label_X1_dim = customtkinter.CTkLabel(
            self, text="Розмірність X1:")
        self.label_X1_dim.grid(row=2, column=0, padx=5, pady=10, sticky="e")
        self.entry_X1_dim = customtkinter.CTkEntry(
            self, width=40, textvariable=self.X1_dim)
        self.entry_X1_dim.grid(row=2, column=1, padx=(
            5, 30), pady=10, sticky="w", columnspan=1)

        self.X2_dim = tkinter.StringVar(value='2')
        self.label_X2_dim = customtkinter.CTkLabel(
            self, text="Розмірність X2:")
        self.label_X2_dim.grid(row=3, column=0, padx=5, pady=10, sticky="e")
        self.entry_X2_dim = customtkinter.CTkEntry(
            self, width=40, textvariable=self.X2_dim)
        self.entry_X2_dim.grid(row=3, column=1, padx=(
            5, 30), pady=10, sticky="w", columnspan=1)

        self.X3_dim = tkinter.StringVar(value='3')
        self.label_X3_dim = customtkinter.CTkLabel(
            self, text="Розмірність X3:")
        self.label_X3_dim.grid(row=4, column=0, padx=5, pady=10, sticky="e")
        self.entry_X3_dim = customtkinter.CTkEntry(
            self, width=40, textvariable=self.X3_dim)
        self.entry_X3_dim.grid(row=4, column=1, padx=(
            5, 30), pady=10, sticky="w", columnspan=1)

        self.Y_dim = tkinter.StringVar(value='4')
        self.label_Y_dim = customtkinter.CTkLabel(
            self, text="Розмірність Y:")
        self.label_Y_dim.grid(row=5, column=0, padx=5, pady=10, sticky="e")
        self.entry_Y_dim = customtkinter.CTkEntry(
            self, width=40, textvariable=self.Y_dim)
        self.entry_Y_dim.grid(row=5, column=1, padx=(
            5, 30), pady=10, sticky="w", columnspan=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)


class MiscView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._scrollbar.configure(width=0)
        self.grid(row=0, column=4, padx=(5, 10), pady=(30, 5), sticky="nsew")


class PolynomView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._scrollbar.configure(width=0)
        self.grid(row=1, column=3, padx=4, pady=(10, 5), sticky="nsew")

        self.label_polynom_selector = customtkinter.CTkLabel(
            self, text="Вид поліномів:")
        self.label_polynom_selector.grid(row=1, column=0, padx=(5, 5), pady=5)
        self.opt_polynom = customtkinter.CTkOptionMenu(self, values=loc[filepath]['polynomials'],
                                                       command=change_polynom)
        self.opt_polynom.grid(row=1, column=1, pady=5, padx=(0, 5))

        self.X1_deg = tkinter.StringVar(value='3')
        self.label_X1_deg = customtkinter.CTkLabel(
            self, text="Степінь X1:")
        self.label_X1_deg.grid(row=2, column=0, padx=(0, 5), pady=10)
        self.entry_X1_deg = customtkinter.CTkEntry(
            self, width=40, textvariable=self.X1_deg)
        self.entry_X1_deg.grid(row=2, column=1, pady=10, sticky="w")

        self.X2_deg = tkinter.StringVar(value='3')
        self.label_X2_deg = customtkinter.CTkLabel(
            self, text="Степінь X2:")
        self.label_X2_deg.grid(row=3, column=0, padx=(0, 5), pady=10)
        self.entry_X2_deg = customtkinter.CTkEntry(
            self, width=40, textvariable=self.X2_deg)
        self.entry_X2_deg.grid(row=3, column=1, pady=10, sticky="w")

        self.X3_deg = tkinter.StringVar(value='3')
        self.label_X3_deg = customtkinter.CTkLabel(
            self, text="Степінь X3:")
        self.label_X3_deg.grid(row=4, column=0, padx=(0, 5), pady=10)
        self.entry_X3_deg = customtkinter.CTkEntry(
            self, width=40, textvariable=self.X3_deg)
        self.entry_X3_deg.grid(row=4, column=1, pady=10, sticky="w")


class InputView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._scrollbar.configure(width=0)
        self.grid(row=1, column=4, padx=(5, 10), pady=(10, 5), sticky="nsew")
        self.manual_input_button = customtkinter.CTkButton(self, text="Вручну",
                                                           command=manual_input)
        self.manual_input_button.grid(
            row=0, padx=(35, 10), pady=5, sticky="ns")

        self.label_input_file = customtkinter.CTkLabel(
            self, text="Файл з вхідними даними")
        self.label_input_file.grid(
            row=1, columnspan=2, padx=10, pady=3, sticky="w")

        search_image = customtkinter.CTkImage(light_image=Image.open(SEARCH_ICON),
                                              dark_image=Image.open(SEARCH_ICON))

        self.entry_file_input = customtkinter.CTkEntry(
            self, width=165, placeholder_text="input.txt")
        self.entry_file_input.grid(row=2, column=0, pady=(0, 3), sticky="e")
        self.button_file_input = customtkinter.CTkButton(
            self, image=search_image, width=40, text='', command=input_file)
        self.button_file_input.grid(
            row=2, column=1, padx=5, pady=(0, 3), sticky="w")

        self.label_output_file = customtkinter.CTkLabel(
            self, text="Файл з результатами")
        self.label_output_file.grid(
            row=3, columnspan=2, padx=10, pady=(5, 3), sticky="w")

        self.entry_file_output = customtkinter.CTkEntry(
            self, width=165, placeholder_text="output.txt")
        self.entry_file_output.grid(row=4, column=0, pady=(3), sticky="e")
        self.button_file_output = customtkinter.CTkButton(
            self, image=search_image, width=40, text='', command=output_file)
        self.button_file_output.grid(
            row=4, column=1, padx=5, pady=(0, 3), sticky="w")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
