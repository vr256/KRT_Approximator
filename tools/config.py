from dataclasses import dataclass, field

import customtkinter

from tools.utils import singleton

customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")


PATH_LIGHT = "resources/images/image_light.png"
PATH_DARK = "resources/images/image_dark.png"
SEARCH_ICON = "resources/images/search_icon.png"
LOGO_PATH = "resources/images/logo.ico"


@singleton
@dataclass
class AppState:
    # * to avoid circular imports
    from models.model import Locale, Optimizer, Polynomial, Theme

    lang: Locale = field(default=Locale.ENG.value)
    theme: Theme = field(default=Theme.Light.value)
    pol: Polynomial = field(default=Polynomial.Hermite.value)
    opt: Optimizer = field(default=Optimizer.Adam.value)
    # TODO store results here
