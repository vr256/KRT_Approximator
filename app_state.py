import os
from dataclasses import dataclass, field

import customtkinter

from tools.utils import singleton

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")


filepath = os.path.splitext(os.path.basename(__file__))[0]


@singleton
@dataclass
class AppState:
    from tools.config import Locale, Optimizer, Polynomial, Theme
    lang: Locale = field(default=Locale.ENG.value)
    theme: Theme = field(default=Theme.Light.value)
    pol: Polynomial = field(default=Polynomial.Hermite.value)
    opt: Optimizer = field(default=Optimizer.Adam.value)
    # TODO store here results