import os

import customtkinter
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as mse

from maths import main_solution
from models import Locale, Theme
from tools.config import PATH_DARK, PATH_LIGHT, AppState
from tools.utils import load_locale

from .formatter import format_txt_input, get_text_results

current_module = os.path.splitext(os.path.basename(__file__))[0]


def change_theme(new_theme: str):
    AppState().theme = Theme.translate(new_theme).value
    customtkinter.set_appearance_mode(AppState().theme)


def change_locale(new_loc: str):
    AppState().lang = Locale.translate(new_loc).value


def change_latex(flag: bool):
    AppState().latex = flag


def change_plot(plot: str):
    AppState().plot = plot


def make_plots():
    """Draw and store plots"""
    loc = load_locale(current_module)
    cur_y = int(AppState().plot[1:])
    y_true = AppState().y_true[cur_y - 1]
    y_pred = AppState().y_pred[cur_y - 1]

    for background, path in zip(
        ["default", "dark_background"],
        [PATH_LIGHT, PATH_DARK],
    ):
        with plt.style.context(background):
            fig, ax = plt.subplots(1, 1)
            ax.plot(range(1, len(y_true) + 1), y_true, label=loc["true_label"])
            ax.plot(range(1, len(y_pred) + 1), y_pred, label=loc["approx_label"])
            loss = mse(
                y_true if y_true.shape[0] else [0],
                y_pred if y_pred.shape[0] else [0],
            )
            ax.set_title(
                loc["mse"] + f" {loss:.3f}",
                y=1.04,
            )
            ax.legend(
                loc="upper center",
                bbox_to_anchor=(0.5, 1.05),
                ncol=2,
                fancybox=True,
                shadow=True,
            )
            fig.savefig(path)


def find_approx():
    res_x, res_y = format_txt_input()
    if isinstance(res_x, int) or isinstance(res_y, int):
        return -1, -1
    else:
        AppState().x_data, AppState().y_true = res_x, res_y
        (
            AppState().y_pred,
            AppState().res_lam,
            AppState().res_a,
            AppState().res_c,
        ) = main_solution(
            AppState().x_data,
            AppState().y_true,
            method=AppState().opt,
            polynom=AppState().pol,
            degs=AppState().pol_degrees,
        )
        plain_text, latex = get_text_results()
        return plain_text, latex
