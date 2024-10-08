import os
import threading
import tkinter

import customtkinter
from PIL import Image

from src.controllers import (
    change_dims,
    change_latex,
    change_locale,
    change_plot,
    change_pol_degrees,
    change_theme,
    find_approx,
    get_text_results,
    make_plots,
    read_from_file,
)
from src.model import Locale, Theme
from src.tools.config import PATH_DARK, PATH_LIGHT, AppState
from src.tools.utils import load_locale

current_module = os.path.splitext(os.path.basename(__file__))[0]


class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)
        self.loc = load_locale(current_module)
        self.logo_label = customtkinter.CTkLabel(
            self,
            text=self.loc["header"],
            font=customtkinter.CTkFont(size=18, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))
        self.info_label = customtkinter.CTkLabel(
            self,
            text=self.loc["info"],
            anchor="nw",
        )
        self.info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0))

        self.locale_label = customtkinter.CTkLabel(
            self,
            text=self.loc["locale_caption"],
            anchor="w",
        )
        self.locale_label.grid(row=4, column=0, padx=10, pady=(0, 30), sticky="sw")
        self.locale_optionemenu = customtkinter.CTkOptionMenu(
            self,
            values=self.loc["locales"],
            command=self.switch_locale,
        )
        self.locale_optionemenu.grid(row=4, column=0, padx=10, pady=(5, 0), sticky="s")

        self.appearance_mode_label = customtkinter.CTkLabel(
            self,
            text=self.loc["theme_caption"],
            anchor="w",
        )
        self.appearance_mode_label.grid(
            row=5,
            column=0,
            padx=10,
            pady=(10, 3),
            sticky="w",
        )
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self,
            values=self.loc["themes"],
            command=change_theme,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(0, 10))

    def update_locale(self):
        self.loc = load_locale(current_module)
        self.logo_label.configure(text=self.loc["header"])
        self.info_label.configure(text=self.loc["info"])

        self.locale_label.configure(text=self.loc["locale_caption"])
        self.locale_optionemenu.configure(values=self.loc["locales"])
        selected_loc_index = [e.value for e in Locale].index(AppState().lang)
        self.locale_optionemenu.set(self.loc["locales"][selected_loc_index])

        self.appearance_mode_label.configure(text=self.loc["theme_caption"])
        self.appearance_mode_optionemenu.configure(values=self.loc["themes"])
        selected_theme_index = [e.value for e in Theme].index(AppState().theme)
        self.appearance_mode_optionemenu.set(self.loc["themes"][selected_theme_index])

    def switch_locale(self, new_loc: str):
        change_locale(new_loc)
        self._master.update_locale()

    def block_locale_selector(self):
        self.locale_optionemenu.configure(state="disabled")

    def unblock_locale_selector(self):
        self.locale_optionemenu.configure(state="normal")


class MainTabview(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self.loc = load_locale(current_module)
        self.grid(
            row=0,
            rowspan=2,
            column=1,
            columnspan=4,
            padx=(7, 0),
            pady=(7, 0),
            sticky="nsew",
        )
        self.res_tab_caption = self.loc["tabs"]["res_tab"]
        self.plot_tab_caption = self.loc["tabs"]["plot_tab"]
        self.add(self.res_tab_caption)
        self.add(self.plot_tab_caption)
        self.tab(self.plot_tab_caption).grid_columnconfigure(0, weight=1)
        self.tab(self.res_tab_caption).grid_columnconfigure(0, weight=1)

        self.results_textbox = customtkinter.CTkTextbox(self.tab(self.res_tab_caption))
        self.results_textbox.grid(row=0, padx=10, pady=5, sticky="nsew")
        self.results_textbox.pack(side="bottom", fill="both", expand="yes")
        self.plain_text = ""
        self.latex = ""

        plot_image = self.load_plot()
        self.results_plot = customtkinter.CTkLabel(
            self.tab(self.plot_tab_caption),
            text="",
            image=plot_image,
        )
        self.results_plot.pack(side="bottom", fill="both", expand="yes")

    def update_locale(self):
        self.loc = load_locale(current_module)

        self._segmented_button._buttons_dict[self.res_tab_caption].configure(
            text=self.loc["tabs"]["res_tab"]
        )
        self._segmented_button._buttons_dict[self.plot_tab_caption].configure(
            text=self.loc["tabs"]["plot_tab"]
        )
        self.results_plot.configure(image=self.load_plot())
        self._master.latex_switcher.update_latex()
        self.plain_text, self.latex = get_text_results()
        self.update_results_text_box()

    def load_plot(self):
        """Load plot from file to image object"""
        make_plots()
        plot_image = customtkinter.CTkImage(
            light_image=Image.open(PATH_LIGHT),
            dark_image=Image.open(PATH_DARK),
            size=(490, 450),
        )
        return plot_image

    def update_results_text_box(self):
        self.results_textbox.delete("1.0", customtkinter.END)
        self.results_textbox.insert(
            "0.0",
            self.latex if AppState().latex else self.plain_text,
        )


class PlotLabel(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self.loc = load_locale(current_module)
        self.grid(row=3, column=1, sticky="nsew", padx=(7, 0), pady=(12, 10))

        self.label_y_function_selector = customtkinter.CTkLabel(
            self, text=self.loc["plot_caption"]
        )
        self.label_y_function_selector.grid(row=2, padx=(20, 5), pady=5)
        self.label_y_function_selector.place(relx=0.5, rely=0.5, anchor="center")

    def update_locale(self):
        self.loc = load_locale(current_module)
        self.label_y_function_selector.configure(text=self.loc["plot_caption"])


class PlotSelector(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self.loc = load_locale(current_module)
        self.grid(row=3, column=2, sticky="nsew", padx=(7, 0), pady=(12, 10))

        self.cur_y = tkinter.StringVar(value="Y1")
        self.plot_y_function_optionmenu = customtkinter.CTkOptionMenu(
            self,
            variable=self.cur_y,
            values=[f"Y{i+1}" for i in range(AppState().num_y)],
            command=self.update_plot,
        )
        self.plot_y_function_optionmenu.pack(
            side="bottom", fill="both", expand="yes", padx=3, pady=3
        )

    def update_plot(self, new_plot: str):
        self.cur_y.set(new_plot)
        change_plot(new_plot)
        plot_image = self._master.main_tabview.load_plot()
        self._master.main_tabview.results_plot.configure(image=plot_image)
        self._master.main_tabview.results_plot.pack(
            side="bottom", fill="both", expand="yes"
        )


class LatexSwitcher(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self.loc = load_locale(current_module)
        self.grid(row=3, column=3, sticky="nsew", padx=(7, 0), pady=(12, 10))
        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=1, uniform="group1")

        self.render_label = customtkinter.CTkLabel(self, text="Latex")
        self.render_label.grid(row=2, column=0, padx=3, pady=5, sticky="e")

        self.render_var = customtkinter.StringVar(value="off")
        self.latex_switch = customtkinter.CTkSwitch(
            self,
            command=self.update_latex,
            text="",
            variable=self.render_var,
            onvalue="on",
            offvalue="off",
        )
        self.latex_switch.grid(row=2, column=1, padx=3, pady=5, sticky="w")

    def update_latex(self):
        change_latex(self.render_var.get() == "on")
        self._master.input_view.write_to_file()
        self._master.main_tabview.update_results_text_box()


class Approximator(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self.loc = load_locale(current_module)
        self.grid(row=3, column=4, padx=(6, 0), pady=(12, 10), sticky="nsew")
        self.calculate_y_button = customtkinter.CTkButton(
            self,
            text=self.loc["find_approx"],
            command=self.calculate_results,
        )
        self.calculate_y_button.pack(side="bottom", fill="both", expand="yes")

    def update_locale(self):
        self.loc = load_locale(current_module)
        self.calculate_y_button.configure(text=self.loc["find_approx"])

    def calculate_results(self):
        compute_result_thread = threading.Thread(target=self.validate_params)
        compute_result_thread.start()

    def update_dimgs_and_degs(self):
        try:
            degs = [
                int(self._master.polynom_view.__dict__[f"entry_X{i}_deg"].get())
                for i in range(1, AppState().num_x + 1)
            ]
            dims = [
                int(self._master.vector_view.entry_Y_dim.get()),
                int(self._master.vector_view.entry_X1_dim.get()),
            ] + [
                int(self._master.vector_view.__dict__[f"entry_X{i}_dim"].get())
                for i in range(2, AppState().num_x + 1)
            ]

            change_pol_degrees(degs)
            change_dims(dims)
        except ValueError:
            self._master.info_view.show_warning(warning="wrong_entry_input")
            return -1

    def validate_params(self):
        # TODO Is it possible to rewrite it in a less cumbersome way?
        AppState().input_file = self._master.input_view.entry_file_input.get()
        AppState().output_file = self._master.input_view.entry_file_output.get()
        num_y = self._master.vector_view.entry_Y_dim.get()

        if AppState().input_file == "":
            self._master.info_view.show_warning(warning="no_input_file")
        else:
            self._master.info_view.show_warning(warning="no_input_file", disable=True)
            if not self.update_dimgs_and_degs():
                self._master.info_view.show_warning(
                    warning="wrong_entry_input", disable=True
                )

                if not os.path.exists(AppState().input_file):
                    self._master.info_view.show_warning(warning="no_such_input_file")
                else:
                    if AppState().output_file != "" and not os.path.exists(
                        AppState().output_file
                    ):
                        self._master.info_view.show_warning(
                            warning="no_such_output_file"
                        )
                    else:
                        for warning in ["no_such_input_file", "no_such_output_file"]:
                            self._master.info_view.show_warning(
                                warning=warning,
                                disable=True,
                            )

                        res_x, res_y = read_from_file(num_y)
                        if isinstance(res_x, int) or isinstance(res_y, int):
                            self._master.info_view.show_warning(
                                warning="wrong_data_format"
                            )
                        else:
                            self._master.info_view.show_warning(
                                warning="wrong_data_format", disable=True
                            )

                            self.calculate_y_button.configure(state="disabled")
                            self._master.info_view.show_warning(
                                warning="wait", colors=("black", "white")
                            )
                            self._master.sidebar.block_locale_selector()
                            p_text, latex = find_approx(res_x, res_y)
                            self._master.sidebar.unblock_locale_selector()
                            self._master.info_view.show_warning(
                                warning="wait", disable=True
                            )
                            self.calculate_y_button.configure(state="normal")

                            self._master.main_tabview.plain_text = p_text
                            self._master.main_tabview.latex = latex

                        make_plots()
                        self._master.input_view.write_to_file()
                        self._master.latex_switcher.update_latex()
                        plot_image = self._master.main_tabview.load_plot()
                        self._master.main_tabview.results_plot.configure(
                            image=plot_image
                        )
                        self._master.main_tabview.results_plot.pack(
                            side="bottom", fill="both", expand="yes"
                        )
