import customtkinter
import tkinter
from PIL import Image
from event import change_appearance_mode_event, change_func, \
                  calculate_y, make_plots, change_method, \
                  change_polynom, manual_input, input_file, \
                  output_file

PATH_LIGHT = 'image_light.png'
PATH_DARK = 'image_dark.png'

APP = None
SEARCH_ICON_LIGHT = 'search_icon.png'
SEARCH_ICON_DARK = 'search_icon.png'

SYSTEM_SOLUTION_METHODS = ["Псевдооберненої матриці", 
                           "Adam", 
                           "SGD", 
                           "NAG", 
                           "Momentum"]

POLYNOMS = ["Ерміта", 
            "Лежандра", 
            "Лаґерра", 
            "Чебишова"]


class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self, text="Відновлення\nфункцій", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Кольорова тема:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=["Світла", "Темна"],
                                                                        command=change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(0, 10))


class YSelector(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=3, column=1, sticky="nsew", padx=(20, 0), pady=10)
        self.label_y_function_selector = customtkinter.CTkLabel(self, text="Графік функції:")
        self.label_y_function_selector.grid(row=2, column=1, padx=(20, 5), pady=5)
        self.cur_y = tkinter.StringVar(value='Y1')
        self.plot_y_function_optionmenu = customtkinter.CTkOptionMenu(self, variable=self.cur_y, values=['Y1', 'Y2', 'Y3', 'Y4'], 
                                                           command=change_func)
        self.plot_y_function_optionmenu.grid(row=2, column=2, padx=10, pady=5)


class YCalculator(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=3, column=2, padx=(10, 10), pady=10, sticky="nsew")
        self.calculate_y_button = customtkinter.CTkButton(self , text="Знайти наближення",
                                                           command=calculate_y)                                  
        self.calculate_y_button.grid(row=0, padx=(35, 10), pady=5, sticky="nsew")
        self.calculate_y_button.pack(side ="bottom", fill="both", expand="yes")


class MainTabview(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=0, rowspan=2, column=1, columnspan=2, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.add("Результати")
        self.add("Графік")
        self.tab("Графік").grid_columnconfigure(0, weight=1) 
        self.tab("Результати").grid_columnconfigure(0, weight=1)

        # text
        self.results_textbox = customtkinter.CTkTextbox(self.tab("Результати"))
        self.results_textbox.grid(row=0, padx=10, pady=5, sticky="nsew")
        self.results_textbox.pack(side ="bottom", fill="both", expand="yes")

        # plots
        make_plots(key=2)
        my_image = customtkinter.CTkImage(light_image=Image.open(PATH_LIGHT),
                                          dark_image=Image.open(PATH_DARK),
                                          size=(520, 450))
        self.results_plot = customtkinter.CTkLabel(self.tab("Графік"), text='', image=my_image)
        self.results_plot.pack(side ="bottom", fill="both", expand="yes")


class SystemSolver(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=3, column=3, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.label_system_solution_selector = customtkinter.CTkLabel(self, text="Метод вирішення несумісної системи:")
        self.label_system_solution_selector.grid(row=2, column=1, padx=(20, 5), pady=5)
        self.opt_system_method = customtkinter.CTkOptionMenu(self, values=SYSTEM_SOLUTION_METHODS, 
                                                           command=change_method)
        self.opt_system_method.grid(row=2, column=2, padx=10, pady=5)


class VectorView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._scrollbar.configure(width=0)
        self.grid(row=0, column=3, padx=(10, 5), pady=(30, 5), sticky="nsew")

        self.X1_dim = tkinter.StringVar(value='2')
        self.label_X1_dim = customtkinter.CTkLabel(self, text="Розмірність X1:")
        self.label_X1_dim.grid(row=2, column=0, padx=5, pady=10, sticky="e")
        self.entry_X1_dim = customtkinter.CTkEntry(self, width=40, textvariable=self.X1_dim)
        self.entry_X1_dim.grid(row=2, column=1, padx=(5, 30),pady=10, sticky="w", columnspan=1)

        self.X2_dim = tkinter.StringVar(value='2')
        self.label_X2_dim = customtkinter.CTkLabel(self, text="Розмірність X2:")
        self.label_X2_dim.grid(row=3, column=0, padx=5, pady=10, sticky="e")
        self.entry_X2_dim = customtkinter.CTkEntry(self, width=40, textvariable=self.X2_dim)
        self.entry_X2_dim.grid(row=3, column=1, padx=(5, 30),pady=10, sticky="w", columnspan=1)

        self.X3_dim = tkinter.StringVar(value='3')
        self.label_X3_dim = customtkinter.CTkLabel(self, text="Розмірність X3:")
        self.label_X3_dim.grid(row=4, column=0, padx=5, pady=10, sticky="e")
        self.entry_X3_dim = customtkinter.CTkEntry(self, width=40, textvariable=self.X3_dim)
        self.entry_X3_dim.grid(row=4, column=1, padx=(5, 30),pady=10, sticky="w", columnspan=1)

        self.Y_dim = tkinter.StringVar(value='4')
        self.label_Y_dim = customtkinter.CTkLabel(self, text="Розмірність Y:")
        self.label_Y_dim.grid(row=5, column=0, padx=5, pady=10, sticky="e")
        self.entry_Y_dim = customtkinter.CTkEntry(self, width=40, textvariable=self.Y_dim)
        self.entry_Y_dim.grid(row=5, column=1, padx=(5, 30), pady=10, sticky="w", columnspan=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)   


class AdditionalView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._scrollbar.configure(width=0)
        self.grid(row=0, column=4, padx=(5, 10), pady=(30, 5), sticky="nsew")

        self.weights_radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(self, text="Ваги цільових функцій")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_avg = customtkinter.CTkRadioButton(self, radiobutton_width=17, radiobutton_height=17, text="Середнє", variable=self.weights_radio_var, value=0)
        self.radio_button_avg.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_maxmin = customtkinter.CTkRadioButton(self, radiobutton_width=17, radiobutton_height=17, text="MaxMin", variable=self.weights_radio_var, value=1)
        self.radio_button_maxmin.grid(row=2, column=2, pady=10, padx=20, sticky="n")


class PolynomView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._scrollbar.configure(width=0)
        self.grid(row=1, column=3, padx=(10, 5), pady=(10, 5), sticky="nsew")
        
        self.label_polynom_selector = customtkinter.CTkLabel(self, text="Вид поліномів:")
        self.label_polynom_selector.grid(row=1, column=0, padx=10, pady=5)
        self.opt_polynom = customtkinter.CTkOptionMenu(self, values=POLYNOMS, 
                                                           command=change_polynom)
        self.opt_polynom.grid(row=1, column=1, pady=5)
        
        self.X1_deg = tkinter.StringVar(value='3')
        self.label_X1_deg = customtkinter.CTkLabel(self, text="Степінь X1:")
        self.label_X1_deg.grid(row=2, column=0, padx=(0, 5), pady=10)
        self.entry_X1_deg = customtkinter.CTkEntry(self, width=40, textvariable=self.X1_deg)
        self.entry_X1_deg.grid(row=2, column=1, pady=10, sticky="w")

        self.X2_deg = tkinter.StringVar(value='3')
        self.label_X2_deg = customtkinter.CTkLabel(self, text="Степінь X2:")
        self.label_X2_deg.grid(row=3, column=0, padx=(0, 5), pady=10)
        self.entry_X2_deg = customtkinter.CTkEntry(self, width=40, textvariable=self.X2_deg)
        self.entry_X2_deg.grid(row=3, column=1, pady=10, sticky="w")

        self.X3_deg = tkinter.StringVar(value='3')
        self.label_X3_deg = customtkinter.CTkLabel(self, text="Степінь X3:")
        self.label_X3_deg.grid(row=4, column=0, padx=(0, 5), pady=10)
        self.entry_X3_deg = customtkinter.CTkEntry(self, width=40, textvariable=self.X3_deg)
        self.entry_X3_deg.grid(row=4, column=1, pady=10, sticky="w")

        
class InputView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._scrollbar.configure(width=0)
        self.grid(row=1, column=4, padx=(5, 10), pady=(10, 5), sticky="nsew")
        self.manual_input_button = customtkinter.CTkButton(self , text="Вручну",
                                                           command=manual_input)                                  
        self.manual_input_button.grid(row=0, padx=(35, 10), pady=5, sticky="ns")

        self.label_input_file = customtkinter.CTkLabel(self, text="Файл з вхідними даними")
        self.label_input_file.grid(row=1, columnspan=2, padx=10, pady=3, sticky="w")

        search_image = customtkinter.CTkImage(light_image=Image.open(SEARCH_ICON_LIGHT), 
                                              dark_image=Image.open(SEARCH_ICON_DARK))

        self.entry_file_input = customtkinter.CTkEntry(self, width=165, placeholder_text="input.txt")
        self.entry_file_input.grid(row=2, column=0, pady=(0, 3), sticky="e")
        self.button_file_input = customtkinter.CTkButton(self, image=search_image, width=50, text='', command=input_file)
        self.button_file_input.grid(row=2, column=1, padx=5, pady=(0, 3), sticky="w")

        self.label_output_file = customtkinter.CTkLabel(self, text="Файл з результатами")
        self.label_output_file.grid(row=3, columnspan=2, padx=10, pady=(5, 3), sticky="w")
        
        self.entry_file_output= customtkinter.CTkEntry(self, width=165, placeholder_text="output.txt")
        self.entry_file_output.grid(row=4, column=0, pady=( 3), sticky="e")
        self.button_file_output = customtkinter.CTkButton(self, image=search_image, width=50, text='', command=output_file)
        self.button_file_output.grid(row=4, column=1, padx=5, pady=(0, 3), sticky="w")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1) 