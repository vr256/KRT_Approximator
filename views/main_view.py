import os

import customtkinter

from tools.utils import load_locale

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

        super().__init__()
        self.loc = load_locale(current_module)

        # window
        self.title(self.loc["title"])
        self.tk.call("tk", "scaling", 1)
        customtkinter.set_widget_scaling(1)
        customtkinter.set_window_scaling(1)
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("blue")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width, window_height = 1400, 600

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")
        self.resizable(False, False)

        # grid layout
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=4)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # contents
        self.sidebar = Sidebar(
            master=self,
            width=130,
            corner_radius=0,
        )
        self.plot_selector = PlotSelector(
            master=self,
            width=300,
        )
        self.approximator = Approximator(
            master=self,
            width=140,
        )
        self.main_tabview = MainTabview(
            master=self,
            width=440,
        )
        self.optimizer = Optimizer(master=self)
        self.vector_view = VectorView(
            master=self,
            label_text=self.loc["vectorView"],
            width=95,
        )
        self.polynom_view = PolynomView(
            master=self,
            label_text=self.loc["polynomView"],
            width=95,
        )
        self.info_view = InfoView(
            master=self,
            label_text=self.loc["infoView"],
            width=150,
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
