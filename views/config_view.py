import os
import tkinter
from functools import partial

import customtkinter
from PIL import Image

from controllers import (
    change_input_file,
    change_optimizer,
    change_output_file,
    change_polynom,
)
from models import Polynomial
from tools.config import ADD_ICON, REMOVE_ICON, SEARCH_ICON, AppState
from tools.utils import load_locale

current_module = os.path.splitext(os.path.basename(__file__))[0]


class VectorView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self.loc = load_locale(current_module)
        self._scrollbar.configure(width=14)
        self.grid(row=0, column=3, padx=(8, 4), pady=(27, 4), sticky="nsew")

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        add_image = customtkinter.CTkImage(
            light_image=Image.open(ADD_ICON),
            dark_image=Image.open(ADD_ICON),
        )
        self.remove_image = customtkinter.CTkImage(
            light_image=Image.open(REMOVE_ICON),
            dark_image=Image.open(REMOVE_ICON),
        )

        self.Y_dim = tkinter.StringVar(value="4")
        self.label_Y_dim = customtkinter.CTkLabel(
            self,
            text=self.loc["dim"] + " Y:  ",
        )
        self.label_Y_dim.grid(row=2, column=0, padx=5, pady=3, sticky="e")
        self.entry_Y_dim = customtkinter.CTkEntry(
            self,
            width=40,
            textvariable=self.Y_dim,
        )
        self.entry_Y_dim.grid(
            row=2,
            column=1,
            padx=(5, 0),
            pady=7,
            sticky="w",
        )
        self.button_remove_Y = customtkinter.CTkButton(
            self,
            image=self.remove_image,
            width=8,
            text="",
            command=partial(self.remove_vector, index=0),
            state="disabled",
            fg_color="gray",
        )
        self.button_remove_Y.grid(
            row=2,
            column=2,
            padx=(7, 10),
            pady=7,
            sticky="we",
        )

        self.X1_dim = tkinter.StringVar(value="2")
        self.label_X1_dim = customtkinter.CTkLabel(self, text=self.loc["dim"] + " X1:")
        self.label_X1_dim.grid(row=3, column=0, padx=5, pady=3, sticky="e")
        self.entry_X1_dim = customtkinter.CTkEntry(
            self,
            width=40,
            textvariable=self.X1_dim,
        )
        self.entry_X1_dim.grid(
            row=3,
            column=1,
            padx=5,
            pady=10,
            sticky="w",
        )
        self.button_remove_X1 = customtkinter.CTkButton(
            self,
            image=self.remove_image,
            width=8,
            text="",
            command=partial(self.remove_vector, index=1),
            state="disabled",
            fg_color="gray",
        )
        self.button_remove_X1.grid(
            row=3,
            column=2,
            padx=(7, 10),
            pady=7,
            sticky="we",
        )

        for i in range(2, AppState().num_x + 1):
            self.__dict__[f"X{i}_dim"] = tkinter.StringVar(value="2")
            self.__dict__[f"label_X{i}_dim"] = customtkinter.CTkLabel(
                self,
                text=self.loc["dim"] + f" X{i}:",
            )
            self.__dict__[f"label_X{i}_dim"].grid(
                row=2 + i,
                column=0,
                padx=5,
                pady=3,
                sticky="e",
            )
            self.__dict__[f"entry_X{i}_dim"] = customtkinter.CTkEntry(
                self,
                width=40,
                textvariable=self.__dict__[f"X{i}_dim"],
            )
            self.__dict__[f"entry_X{i}_dim"].grid(
                row=2 + i,
                column=1,
                padx=5,
                pady=10,
                sticky="w",
            )
            self.__dict__[f"button_remove_X{i}"] = customtkinter.CTkButton(
                self,
                image=self.remove_image,
                width=8,
                text="",
                command=partial(self.remove_vector, index=i),
            )
            self.__dict__[f"button_remove_X{i}"].grid(
                row=2 + i,
                column=2,
                padx=(7, 10),
                pady=7,
                sticky="we",
            )

        self.button_add_vector = customtkinter.CTkButton(
            self,
            image=add_image,
            width=70,
            text="",
            command=self.add_vector,
        )
        self.button_add_vector.grid(
            row=3 + AppState().num_x,
            column=0,
            columnspan=3,
            padx=12,
            pady=7,
            sticky="we",
        )

    def update_locale(self):
        self.loc = load_locale(current_module)
        for i in range(1, AppState().num_x + 1):
            self.__dict__[f"label_X{i}_dim"].configure(text=self.loc["dim"] + f" X{i}:")
        self.label_Y_dim.configure(text=self.loc["dim"] + " Y:  ")

    def add_vector(self):
        AppState().num_x += 1
        # Shifting add button
        self.button_add_vector.grid(
            row=3 + AppState().num_x,
            column=0,
            columnspan=3,
            padx=12,
            pady=7,
            sticky="we",
        )
        # Adding X vector
        self.__dict__[f"X{AppState().num_x}_dim"] = tkinter.StringVar(value="2")
        self.__dict__[f"label_X{AppState().num_x}_dim"] = customtkinter.CTkLabel(
            self,
            text=self.loc["dim"] + f" X{AppState().num_x}:",
        )
        self.__dict__[f"label_X{AppState().num_x}_dim"].grid(
            row=2 + AppState().num_x,
            column=0,
            padx=5,
            pady=3,
            sticky="e",
        )
        self.__dict__[f"entry_X{AppState().num_x}_dim"] = customtkinter.CTkEntry(
            self,
            width=40,
            textvariable=self.__dict__[f"X{AppState().num_x}_dim"],
        )
        self.__dict__[f"entry_X{AppState().num_x}_dim"].grid(
            row=2 + AppState().num_x,
            column=1,
            padx=5,
            pady=10,
            sticky="w",
        )
        self.__dict__[f"button_remove_X{AppState().num_x}"] = customtkinter.CTkButton(
            self,
            image=self.remove_image,
            width=8,
            text="",
            command=partial(self.remove_vector, index=AppState().num_x),
        )
        self.__dict__[f"button_remove_X{AppState().num_x}"].grid(
            row=2 + AppState().num_x,
            column=2,
            padx=(7, 10),
            pady=7,
            sticky="we",
        )
        # Revise polynomial view
        self._master.polynom_view.update_after_add()

    def remove_vector(self, index: int):
        # Removing given vector
        self.__dict__[f"label_X{index}_dim"].destroy()
        self.__dict__[f"entry_X{index}_dim"].destroy()
        self.__dict__[f"button_remove_X{index}"].destroy()
        # Shifting other vectors
        for i in range(index, AppState().num_x):
            self.__dict__[f"label_X{i}_dim"] = self.__dict__[f"label_X{i + 1}_dim"]
            self.__dict__[f"label_X{i}_dim"].configure(text=self.loc["dim"] + f" X{i}:")
            self.__dict__[f"label_X{i}_dim"].grid(row=2 + i)

            self.__dict__[f"entry_X{i}_dim"] = self.__dict__[f"entry_X{i + 1}_dim"]
            self.__dict__[f"entry_X{i}_dim"].grid(row=2 + i)

            self.__dict__[f"button_remove_X{i}"] = self.__dict__[
                f"button_remove_X{i + 1}"
            ]
            self.__dict__[f"button_remove_X{i}"].grid(row=2 + i)
            self.__dict__[f"button_remove_X{i}"].configure(
                command=partial(self.remove_vector, index=i),
            )

        # Removing now-redundant vector
        self.__dict__.pop(f"label_X{AppState().num_x}_dim")
        self.__dict__.pop(f"entry_X{AppState().num_x}_dim")
        self.__dict__.pop(f"button_remove_X{AppState().num_x}")
        # Revise polynomial view
        self._master.polynom_view.update_after_remove(index)


class PolynomView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.loc = load_locale(current_module)
        self._scrollbar.configure(width=14)
        self.grid(row=1, column=3, padx=(8, 4), pady=(8, 0), sticky="nsew")

        self.label_polynom_selector = customtkinter.CTkLabel(
            self,
            text=self.loc["pol_kind"],
        )
        self.label_polynom_selector.grid(row=1, column=0, padx=(30, 5), pady=(10, 5))
        self.opt_polynom = customtkinter.CTkOptionMenu(
            self,
            values=self.loc["polynomials"],
            command=change_polynom,
            width=120,
        )
        self.opt_polynom.grid(row=1, column=1, padx=(0, 5), pady=5)

        for i in range(1, AppState().num_x + 1):
            self.__dict__[f"X{i}_deg"] = tkinter.StringVar(value="3")
            self.__dict__[f"label_X{i}_deg"] = customtkinter.CTkLabel(
                self,
                text=self.loc["deg"] + f" X{i}:",
            )
            self.__dict__[f"label_X{i}_deg"].grid(
                row=1 + i,
                column=0,
                padx=(30, 10),
                pady=10,
            )
            self.__dict__[f"entry_X{i}_deg"] = customtkinter.CTkEntry(
                self,
                width=40,
                textvariable=self.__dict__[f"X{i}_deg"],
            )
            self.__dict__[f"entry_X{i}_deg"].grid(
                row=1 + i,
                column=1,
                padx=(0, 5),
                pady=10,
                sticky="w",
            )

    def update_locale(self):
        self.loc = load_locale(current_module)
        self.label_polynom_selector.configure(text=self.loc["pol_kind"])
        self.opt_polynom.configure(values=self.loc["polynomials"])
        selected_pol_index = [e.value for e in Polynomial].index(AppState().pol)
        self.opt_polynom.set(self.loc["polynomials"][selected_pol_index])
        for i in range(1, AppState().num_x + 1):
            self.__dict__[f"label_X{i}_deg"].configure(text=self.loc["deg"] + f" X{i}:")

    def update_after_add(self):
        self.__dict__[f"X{AppState().num_x}_deg"] = tkinter.StringVar(value="3")
        self.__dict__[f"label_X{AppState().num_x}_deg"] = customtkinter.CTkLabel(
            self,
            text=self.loc["deg"] + f" X{AppState().num_x}:",
        )
        self.__dict__[f"label_X{AppState().num_x}_deg"].grid(
            row=1 + AppState().num_x,
            column=0,
            padx=(30, 10),
            pady=10,
        )
        self.__dict__[f"entry_X{AppState().num_x}_deg"] = customtkinter.CTkEntry(
            self,
            width=40,
            textvariable=self.__dict__[f"X{AppState().num_x}_deg"],
        )
        self.__dict__[f"entry_X{AppState().num_x}_deg"].grid(
            row=1 + AppState().num_x,
            column=1,
            padx=(0, 5),
            pady=10,
            sticky="w",
        )

    def update_after_remove(self, index: int):
        # Removing given vector
        self.__dict__[f"label_X{index}_deg"].destroy()
        self.__dict__[f"entry_X{index}_deg"].destroy()
        # Shifting other vectors
        for i in range(index, AppState().num_x):
            self.__dict__[f"label_X{i}_deg"] = self.__dict__[f"label_X{i + 1}_deg"]
            self.__dict__[f"label_X{i}_deg"].configure(text=self.loc["deg"] + f" X{i}:")
            self.__dict__[f"label_X{i}_deg"].grid(row=2 + i)
            self.__dict__[f"entry_X{i}_deg"] = self.__dict__[f"entry_X{i + 1}_deg"]
            self.__dict__[f"entry_X{i}_deg"].grid(row=2 + i)
        # Removing now-redundant vector
        self.__dict__.pop(f"label_X{AppState().num_x}_deg")
        self.__dict__.pop(f"entry_X{AppState().num_x}_deg")
        AppState().num_x -= 1


class InfoView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.loc = load_locale(current_module)["info"]
        self._scrollbar.configure(width=0)
        self.grid(row=0, column=4, padx=(4, 8), pady=(27, 4), sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.n_labels = 0
        self._warnings = (
            "no_input_file",
            "no_such_input_file",
            "no_such_output_file",
            "wrong_data_format",
        )

    def update_locale(self):
        self.loc = load_locale(current_module)["info"]
        for label in self._warnings:
            if label in self.__dict__:
                self.__dict__[label].configure(text=self.loc[label])

    def show_warning(self, warning, destroy=False):
        if not destroy:
            if warning not in self.__dict__:
                self.__dict__[warning] = customtkinter.CTkLabel(
                    self,
                    text=self.loc[warning],
                    text_color=("red", "yellow"),
                )
                self.__dict__[warning].grid(row=self.n_labels, column=0)
                self.n_labels += 1
                self.rowconfigure(self.n_labels, weight=1)
        else:
            if warning in self.__dict__:
                self.__dict__[warning].destroy()
                self.__dict__.pop(warning)


class InputView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._master = master
        self.loc = load_locale(current_module)
        self._scrollbar.configure(width=0)
        self.grid(row=1, column=4, padx=(4, 8), pady=(8, 0), sticky="nsew")

        self.label_input_file = customtkinter.CTkLabel(
            self,
            text=self.loc["input_file"],
        )
        self.label_input_file.grid(row=1, columnspan=2, padx=10, pady=3, sticky="w")

        search_image = customtkinter.CTkImage(
            light_image=Image.open(SEARCH_ICON),
            dark_image=Image.open(SEARCH_ICON),
        )

        self.entry_file_input = customtkinter.CTkEntry(
            self,
            width=165,
            placeholder_text="input.txt",
        )
        self.entry_file_input.grid(row=2, column=0, pady=(0, 3), sticky="e")
        self.button_file_input = customtkinter.CTkButton(
            self,
            image=search_image,
            width=40,
            text="",
            command=self.update_input_file,
        )
        self.button_file_input.grid(row=2, column=1, padx=5, pady=(0, 3), sticky="w")

        self.label_output_file = customtkinter.CTkLabel(
            self,
            text=self.loc["output_file"],
        )
        self.label_output_file.grid(
            row=3,
            columnspan=2,
            padx=10,
            pady=(5, 3),
            sticky="w",
        )

        self.entry_file_output = customtkinter.CTkEntry(
            self,
            width=165,
            placeholder_text="output.txt",
        )
        self.entry_file_output.grid(row=4, column=0, pady=(3), sticky="e")
        self.button_file_output = customtkinter.CTkButton(
            self,
            image=search_image,
            width=40,
            text="",
            command=self.update_output_file,
        )
        self.button_file_output.grid(row=4, column=1, padx=5, pady=(0, 3), sticky="w")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def update_locale(self):
        self.loc = load_locale(current_module)
        self.label_input_file.configure(text=self.loc["input_file"])
        self.label_output_file.configure(text=self.loc["output_file"])

    def update_input_file(self):
        path = customtkinter.filedialog.askopenfilename()
        if os.path.exists(path):
            for warning in ["no_such_input_file", "no_input_file", "wrong_data_format"]:
                self._master.info_view.show_warning(
                    warning=warning,
                    destroy=True,
                )
            self.entry_file_input.delete(0, "end")
            self.entry_file_input.insert(0, path)
            change_input_file(path)

    def update_output_file(self):
        path = customtkinter.filedialog.askopenfilename()
        if os.path.exists(path):
            self._master.info_view.show_warning(
                warning="no_such_output_file",
                destroy=True,
            )
            self.entry_file_output.delete(0, "end")
            self.entry_file_output.insert(0, path)
            change_output_file(path)
            self.write_to_file()

    def write_to_file(self):
        if (
            hasattr(AppState(), "output_file")
            and hasattr(self._master.main_tabview, "plain_text")
            and isinstance(
                AppState().output_file,
                str,
            )
        ):
            if AppState().output_file != "" and not os.path.exists(
                AppState().output_file,
            ):
                self._master.info_view.show_warning(warning="no_such_output_file")
            else:
                self._master.info_view.show_warning(
                    warning="no_such_output_file",
                    destroy=True,
                )
                if AppState().output_file != "":
                    with open(AppState().output_file, "w", encoding="utf-8") as file:
                        file.write(
                            self._master.main_tabview.latex
                            if AppState().latex
                            else self._master.main_tabview.plain_text,
                        )


class Optimizer(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.loc = load_locale(current_module)
        self.grid(row=3, column=3, columnspan=2, sticky="nsew", padx=8, pady=12)
        self.label_system_solution_selector = customtkinter.CTkLabel(
            self,
            text=self.loc["optimizer_caption"],
        )
        self.label_system_solution_selector.grid(row=2, column=1, padx=(20, 5), pady=5)
        self.opt_system_method = customtkinter.CTkOptionMenu(
            self,
            values=self.loc["optimizers"],
            command=change_optimizer,
        )
        self.opt_system_method.grid(row=2, column=2, padx=10, pady=5)

    def update_locale(self):
        self.loc = load_locale(current_module)
        self.label_system_solution_selector.configure(
            text=self.loc["optimizer_caption"],
        )
        self.opt_system_method.configure(values=self.loc["optimizers"])
