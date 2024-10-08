from dataclasses import dataclass, field

import customtkinter
import numpy as np

from src.tools.utils import singleton

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")


PATH_LIGHT = "src/resources/images/image_light.png"
PATH_DARK = "src/resources/images/image_dark.png"
SEARCH_ICON = "src/resources/images/search_icon.png"
ADD_ICON = "src/resources/images/add_icon.png"
REMOVE_ICON = "src/resources/images/remove_icon.png"
LOGO_PATH = "src/resources/images/logo.ico"


def init_array():
    return np.array([[] for _ in range(4)])


@singleton
@dataclass
class AppState:
    # * to avoid circular imports
    from src.model import Locale, Optimizer, Polynomial, Theme

    # Option menus
    lang: Locale = field(default=Locale.ENG.value)
    theme: Theme = field(default=Theme.Light.value)
    pol: Polynomial = field(default=Polynomial.Hermite.value)
    opt: Optimizer = field(default=Optimizer.Adam.value)
    plot: str = field(default="Y1")

    # Entry forms
    num_y: int = field(default=4)
    num_x: int = field(default=3)
    dims: tuple[int] = field(default=(4, 2, 2, 3))
    pol_degrees: tuple[int] = field(default=(3, 3, 3))
    input_file: str = field(init=False)
    output_file: str = field(default=None)

    # Checkboxes
    latex: bool = field(default=False)

    # Results
    x_data: list = field(init=False, repr=False)
    y_true: np.ndarray = field(default_factory=init_array, repr=False)
    y_pred: np.ndarray = field(default_factory=init_array, repr=False)
    res_lam: np.ndarray = field(init=False, repr=False)
    res_a: np.ndarray = field(init=False, repr=False)
    res_c: np.ndarray = field(init=False, repr=False)
