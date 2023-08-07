import json
import os

import customtkinter

from app_state import AppState

customtkinter.set_appearance_mode('Light')
customtkinter.set_default_color_theme('blue')


current_module = os.path.splitext(os.path.basename(__file__))[0]


def load_locale(path):
    with open(AppState.lang, 'r', encoding='utf-8') as file:
        loc = json.load(file)[path]
        return loc


class App(customtkinter.CTk):
    def __init__(self):
        # * to avoid circular imports
        from views import (
            InputView,
            MainTabview,
            MiscView,
            Optimizer,
            PolynomView,
            Sidebar,
            VectorView,
            YCalculator,
            YSelector,
        )
        super().__init__()
        self.loc = load_locale(current_module)

        # window
        self.title(self.loc['title'])
        self.geometry(f'{1400}x{600}')

        # grid layout
        self.grid_columnconfigure(1, weight=20)
        self.grid_columnconfigure(2, weight=30)
        self.grid_columnconfigure(3, weight=40)
        self.grid_columnconfigure(4, weight=10)
        self.grid_rowconfigure((0, 1, 2), weight=10)

        # contents
        self.sidebar = Sidebar(master=self, width=130, corner_radius=0)
        self.y_selector = YSelector(master=self)
        self.calculate_y = YCalculator(master=self)
        self.main_tabview = MainTabview(master=self, width=440)
        self.system_solver = Optimizer(master=self)
        self.vector_view = VectorView(master=self, label_text=self.loc['vectorView'], width=95)
        self.polynom_view = PolynomView(master=self, label_text=self.loc['polynomView'], width=95)
        self.misc_view = MiscView(master=self, label_text=self.loc['misclView'], width=150)
        self.input_view = InputView(master=self, label_text=self.loc['inputView'])

        self.widgets = (self.sidebar, self.y_selector, self.calculate_y, self.main_tabview,
                        self.system_solver, self.vector_view, self.polynom_view,
                        self.misc_view, self.input_view)

    def update_locale(self):
        self.loc = load_locale(current_module)
        self.vector_view.configure(label_text=self.loc['vectorView'])
        self.polynom_view.configure(label_text=self.loc['polynomView'])
        self.misc_view.configure(label_text=self.loc['misclView'])
        self.input_view.configure(label_text=self.loc['inputView'])
        for widget in self.widgets:
            widget.update_locale()
