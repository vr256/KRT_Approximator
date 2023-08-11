import os

import customtkinter

from tools.config import H_COEF, W_COEF
from tools.utils import load_locale

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")


current_module = os.path.splitext(os.path.basename(__file__))[0]


class App(customtkinter.CTk):
    def __init__(self):
        # * to avoid circular imports
        from views import (
            Approximator,
            InfoView,
            InputView,
            MainTabview,
            Optimizer,
            PlotSelector,
            PolynomView,
            Sidebar,
            VectorView,
        )

        global W_COEF, H_COEF
        super().__init__()
        self.loc = load_locale(current_module)

        # window
        self.title(self.loc["title"])
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        W_COEF = screen_width / 1920
        H_COEF = screen_height / 1080
        window_width = int(1400 * W_COEF)
        window_height = int(600 * H_COEF)
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        self.resizable(False, False)

        # grid layout
        self.grid_columnconfigure(1, weight=20)
        self.grid_columnconfigure(2, weight=30)
        self.grid_columnconfigure(3, weight=40)
        self.grid_columnconfigure(4, weight=10)
        self.grid_rowconfigure((0, 1, 2), weight=10)

        # contents
        self.sidebar = Sidebar(
            master=self,
            width=int(130 * W_COEF),
            corner_radius=0,
        )
        self.plot_selector = PlotSelector(
            master=self,
            width=int(300 * W_COEF),
        )
        self.approximator = Approximator(
            master=self,
            width=int(140 * W_COEF),
        )
        self.main_tabview = MainTabview(
            master=self,
            width=int(440 * W_COEF),
        )
        self.optimizer = Optimizer(master=self)
        self.vector_view = VectorView(
            master=self,
            label_text=self.loc["vectorView"],
            width=int(95 * W_COEF),
        )
        self.polynom_view = PolynomView(
            master=self,
            label_text=self.loc["polynomView"],
            width=int(95 * W_COEF),
        )
        self.info_view = InfoView(
            master=self,
            label_text=self.loc["infoView"],
            width=int(150 * W_COEF),
        )
        self.input_view = InputView(master=self, label_text=self.loc["inputView"])

        self.widgets = (
            self.sidebar,
            self.approximator,
            self.plot_selector,
            self.main_tabview,
            self.optimizer,
            self.vector_view,
            self.polynom_view,
            self.info_view,
            self.input_view,
        )

    def update_locale(self):
        self.loc = load_locale(current_module)
        self.vector_view.configure(label_text=self.loc["vectorView"])
        self.polynom_view.configure(label_text=self.loc["polynomView"])
        self.info_view.configure(label_text=self.loc["infoView"])
        self.input_view.configure(label_text=self.loc["inputView"])
        for widget in self.widgets:
            widget.update_locale()

    def destroy(self):
        exit()
