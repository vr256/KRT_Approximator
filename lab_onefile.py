import tkinter
import tkinter.messagebox
import customtkinter

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
from .menu import Sidebar

customtkinter.set_appearance_mode("Light") 
customtkinter.set_default_color_theme("blue")

CURRENT_THEME = None
CURRENT_Y = None
CURRENT_PRED = {}
PATH_LIGHT = 'image_light.png'
PATH_DARK = 'image_dark.png'

SYSTEM_SOLUTION_METHODS = ["Псевдооберненої матриці", 
                           "Adam", 
                           "SGD", 
                           "NAG", 
                           "Momentum"]


SAMPLE_STRING = '''
 =0,2961* +0,0621* –0,0058* –0,0024* –
–0,2851* +0,1783* +0,0222* +0,0000* –
–0,0313* +0,0053* –0,0025* +0,0001* –
–0,0304* –0,0173* –0,0056* –0,0000* +
+0,2220* +0,1639* +0,0409* –0,0104* +
+0,2193* +0,0529* –0,0171* +0,0000* ;

 =0,3133* +0,0657* –0,0061* –0,0025* +
+0,3204* +0,2004* +0,0250* +0,0000* –
–0,0265* –0,0045* –0,0021* +0,0001* –
–0,0258* –0,0147* –0,0048* –0,0000* +
+0,2067* +0,1526* +0,0381* –0,0097* +
+0,2089* +0,0504* –0,0163* +0,0000* ;

 =0,3210* +0,0674* –0,0063* –0,0026* +
+0,3355* +0,2099* +0,0262* +0,0000* –
–0,0266* –0,0045* –0,0021* +0,0001* –
–0,0259* –0,0148* –0,0048* –0,0000* +
+0,2023* +0,1493* +0,0373* –0,0095* +
+0,2062* +0,0498* –0,0161* +0,0000* ;

 =0,3199* +0,0671* –0,0062* –0,0026* +
+0,3301* +0,2065* +0,0257* +0,0000* –
–0,0309* –0,0052* –0,0025* +0,0001* –
–0,0301* –0,0172* –0,0056* –0,0000* +
+0,2081* +0,1536* +0,0384* –0,0097* +
+0,2117* +0,0510* –0,0165* +0,0000* 

'''

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("СА Лабораторна робота №2")
        self.geometry(f"{1300}x{600}")

        # configure grid layout
        self.grid_columnconfigure((1, 2), weight=30)
        self.grid_columnconfigure(3, weight=20)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # column 0
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Відновлення\nфункцій", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Кольорова тема:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Світла", "Темна"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(0, 10))

        # Y function selector
        self.y_function_selector = customtkinter.CTkFrame(self)
        self.y_function_selector.grid(row=3, column=1, sticky="nsew", padx=(20, 0), pady=10)
        self.label_y_function_selector = customtkinter.CTkLabel(self.y_function_selector, text="Графік функції:")
        self.label_y_function_selector.grid(row=2, column=1, padx=(20, 5), pady=5)
        self.plot_y_function_optionmenu = customtkinter.CTkOptionMenu(self.y_function_selector, values=["Y1", "Y2", "Y3"], 
                                                           command=self.change_func)
        self.plot_y_function_optionmenu.grid(row=2, column=2, padx=10, pady=5)

        # calculate Y button
        self.calculate_y_frame= customtkinter.CTkFrame(self)
        self.calculate_y_frame.grid(row=3, column=2, padx=(10, 10), pady=10, sticky="nsew")
        self.calculate_y_button = customtkinter.CTkButton(self.calculate_y_frame , text="Знайти наближення",
                                                           command=self.calculate)                                  
        self.calculate_y_button.grid(row=0, padx=(35, 10), pady=5, sticky="nsew")
        self.calculate_y_button.pack(side ="bottom", fill="both", expand="yes")

        # MAIN Tabview
        self.main_tabview = customtkinter.CTkTabview(self, width=450)
        self.main_tabview.grid(row=0, rowspan=2, column=1, columnspan=2, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.main_tabview.add("Результати")
        self.main_tabview.add("Графік")
        self.main_tabview.tab("Графік").grid_columnconfigure(0, weight=1) 
        self.main_tabview.tab("Результати").grid_columnconfigure(0, weight=1)

        # text
        self.results_textbox = customtkinter.CTkTextbox(self.main_tabview.tab("Результати"))
        self.results_textbox.grid(row=0, padx=10, pady=5, sticky="nsew")
        self.results_textbox.pack(side ="bottom", fill="both", expand="yes")
        self.results_textbox.insert('0.0', SAMPLE_STRING)

        # plots
        self.make_plots(key=2)
        my_image = customtkinter.CTkImage(light_image=Image.open(PATH_LIGHT),
                                  dark_image=Image.open(PATH_DARK),
                                  size=(520, 450))
        self.results_plot = customtkinter.CTkLabel(self.main_tabview.tab("Графік"), text='', image=my_image)
        self.results_plot.pack(side ="bottom", fill="both", expand="yes")
        
        # method for solving system
        self.system_solution_selector = customtkinter.CTkFrame(self)
        self.system_solution_selector.grid(row=3, column=3, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.label_system_solution_selector = customtkinter.CTkLabel(self.system_solution_selector, text="Метод вирішення несумісної системи:")
        self.label_system_solution_selector.grid(row=2, column=1, padx=(20, 5), pady=5)
        self.opt_system_method = customtkinter.CTkOptionMenu(self.system_solution_selector, values=SYSTEM_SOLUTION_METHODS, 
                                                           command=self.change_method)
        self.opt_system_method.grid(row=2, column=2, padx=10, pady=5)


        # vectors dimensionality
        self.vectors_frame = customtkinter.CTkScrollableFrame(self, label_text="Вектори", width=95)
        self.vectors_frame._scrollbar.configure(width=0)
        self.vectors_frame.grid(row=0, column=3, padx=(10, 5), pady=(30, 5), sticky="nsew")

        self.label_X1_dim = customtkinter.CTkLabel(self.vectors_frame, text="Розмірність X1:")
        self.label_X1_dim.grid(row=2, column=0, padx=5, pady=10, sticky="e")
        self.entry_X1_dim = customtkinter.CTkEntry(self.vectors_frame, width=40, placeholder_text="3")
        self.entry_X1_dim.grid(row=2, column=1, padx=(5, 30),pady=10, sticky="w", columnspan=1)

        self.label_X2_dim = customtkinter.CTkLabel(self.vectors_frame, text="Розмірність X2:")
        self.label_X2_dim.grid(row=3, column=0, padx=5, pady=10, sticky="e")
        self.entry_X2_dim = customtkinter.CTkEntry(self.vectors_frame, width=40, placeholder_text="3")
        self.entry_X2_dim.grid(row=3, column=1, padx=(5, 30),pady=10, sticky="w", columnspan=1)

        self.label_X3_dim = customtkinter.CTkLabel(self.vectors_frame, text="Розмірність X3:")
        self.label_X3_dim.grid(row=4, column=0, padx=5, pady=10, sticky="e")
        self.entry_X3_dim = customtkinter.CTkEntry(self.vectors_frame, width=40, placeholder_text="3")
        self.entry_X3_dim.grid(row=4, column=1, padx=(5, 30),pady=10, sticky="w", columnspan=1)

        self.label_Y_dim = customtkinter.CTkLabel(self.vectors_frame, text="Розмірність Y:")
        self.label_Y_dim.grid(row=5, column=0, padx=5, pady=10, sticky="e")
        self.entry_Y_dim = customtkinter.CTkEntry(self.vectors_frame, width=40, placeholder_text="3")
        self.entry_Y_dim.grid(row=5, column=1, padx=(5, 30), pady=10, sticky="w", columnspan=1)
        self.vectors_frame.columnconfigure(0, weight=2)
        self.vectors_frame.columnconfigure(1, weight=1)        

        # polynoms
        self.polynom_frame = customtkinter.CTkScrollableFrame(self, label_text="Поліноми", width=95)
        self.polynom_frame._scrollbar.configure(width=0)
        self.polynom_frame.grid(row=1, column=3, padx=(10, 5), pady=(10, 5), sticky="nsew")
        
        self.label_polynom_selector = customtkinter.CTkLabel(self.polynom_frame, text="Вид поліномів:")
        self.label_polynom_selector.grid(row=1, column=0, padx=10, pady=5)
        self.opt_polynom = customtkinter.CTkOptionMenu(self.polynom_frame, values=["Ерміта", "Лежандра", "Лаґерра", "Чебишова"], 
                                                           command=self.select_polynom)
        self.opt_polynom.grid(row=1, column=1, pady=5)
        self.label_X1_deg = customtkinter.CTkLabel(self.polynom_frame, text="Степінь X1:")
        self.label_X1_deg.grid(row=2, column=0, padx=(0, 5), pady=10)
        self.entry_X1_deg = customtkinter.CTkEntry(self.polynom_frame, width=40, placeholder_text="3")
        self.entry_X1_deg.grid(row=2, column=1, pady=10, sticky="w")

        self.label_X2_deg = customtkinter.CTkLabel(self.polynom_frame, text="Степінь X2:")
        self.label_X2_deg.grid(row=3, column=0, padx=(0, 5), pady=10)
        self.entry_X2_deg = customtkinter.CTkEntry(self.polynom_frame, width=40, placeholder_text="3")
        self.entry_X2_deg.grid(row=3, column=1, pady=10, sticky="w")

        self.label_X3_deg = customtkinter.CTkLabel(self.polynom_frame, text="Степінь X3:")
        self.label_X3_deg.grid(row=4, column=0, padx=(0, 5), pady=10)
        self.entry_X3_deg = customtkinter.CTkEntry(self.polynom_frame, width=40, placeholder_text="3")
        self.entry_X3_deg.grid(row=4, column=1, pady=10, sticky="w")

        # additional
        self.additional_frame = customtkinter.CTkScrollableFrame(self, label_text="Додатково", width=150)
        self.additional_frame._scrollbar.configure(width=0)
        self.additional_frame.grid(row=0, column=4, padx=(5, 10), pady=(30, 5), sticky="nsew")

        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(self.additional_frame, text="Ваги цільових функцій")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_avg = customtkinter.CTkRadioButton(self.additional_frame, radiobutton_width=17, radiobutton_height=17, text="Середнє", variable=self.radio_var, value=0)
        self.radio_button_avg.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_maxmin = customtkinter.CTkRadioButton(self.additional_frame, radiobutton_width=17, radiobutton_height=17, text="MaxMin", variable=self.radio_var, value=1)
        self.radio_button_maxmin.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        # input
        self.input_view = customtkinter.CTkScrollableFrame(self, label_text="Введення даних")
        self.input_view._scrollbar.configure(width=0)
        self.input_view.grid(row=1, column=4, padx=(5, 10), pady=(10, 0), sticky="nsew")
        self.manual_input_button = customtkinter.CTkButton(self.input_view , text="Вручну",
                                                           command=self.open_input_dialog_event)                                  
        self.manual_input_button.grid(row=0, padx=(35, 10), pady=5, sticky="ns")

        self.label_input_file = customtkinter.CTkLabel(self.input_view, text="Файл з вхідними даними")
        self.label_input_file.grid(row=1, padx=10, pady=3, sticky="nsew")

        self.entry_file_input = customtkinter.CTkEntry(self.input_view, width=40, placeholder_text="input.txt")
        self.entry_file_input.grid(row=2, pady=(0, 3), sticky="nsew")

        self.label_output_file = customtkinter.CTkLabel(self.input_view, text="Файл з результатами")
        self.label_output_file.grid(row=3, padx=10, pady=(5, 3), sticky="nsew")
        
        self.entry_file_output= customtkinter.CTkEntry(self.input_view, width=40, placeholder_text="output.txt")
        self.entry_file_output.grid(row=4, pady=(0, 3), sticky="nsew")

    def select_polynom(self, polynom : str):
        pass

    def calculate(self):
        return

    def change_method(self):
        pass

    def make_plots(self, key=1):
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
            self.results_plot.configure(image=my_image)
            self.results_plot.pack(side ="bottom", fill="both", expand="yes")
            self.results_plot.image=my_image

    def change_func(self, y : str):
        global CURRENT_PRED, CURRENT_Y
        CURRENT_Y = y
        #y_pred = CURRENT_PRED[y]
        self.make_plots()
        
        #self.results_plot = customtkinter.CTkLabel(self.tabview.tab("Графік"), text='', image=my_image)
        #self.results_plot.pack()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        global CURRENT_THEME
        trans = {"Світла": "Light",
                    "Темна": "Dark"}
        customtkinter.set_appearance_mode(trans[new_appearance_mode])
        CURRENT_THEME = trans[new_appearance_mode]
        self.make_plots()
        #CURRENT_PRED, CURRENT_Y
                
        #self.results_plot = customtkinter.CTkLabel(self.tabview.tab("Графік"), text='', image=my_image)
        #self.results_plot.pack()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Введіть вибірку:", title="Введення даних")
        print("Ручний ввід:", dialog.get_input())


if __name__ == "__main__":
    app = App()
    app.mainloop()