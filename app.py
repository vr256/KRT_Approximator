import json
import os
import sys
from dataclasses import dataclass, field

import customtkinter

from tools.utils import singleton

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")


filepath = os.path.splitext(os.path.basename(__file__))[0]


@singleton
@dataclass
class AppState:
    from tools.config import Locale
    lang: Locale = field(default=Locale.ENG)


with open(AppState.lang.value, 'r', encoding='utf-8') as file:
    loc = json.load(file)


class App(customtkinter.CTk):
    def __init__(self):
        from widgets import (
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

        # window
        self.title(loc[filepath]['title'])
        self.geometry(f"{1400}x{600}")

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
        self.vector_view = VectorView(master=self, label_text=loc[filepath]['vectorView'], width=95)
        self.polynom_view = PolynomView(master=self, label_text=loc[filepath]['polynomView'], width=95)
        self.mist_view = MiscView(master=self, label_text=loc[filepath]['additionalView'], width=150)
        self.input_view = InputView(master=self, label_text=loc[filepath]['inputView'])
