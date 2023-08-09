from models import Optimizer, Polynomial
from tools.config import AppState


def change_input_file(path: str):
    AppState().input_file = path


def change_output_file(path: str):
    AppState().output_file = path


def change_polynom(new_pol: str):
    AppState().pol = Polynomial.translate(new_pol).value


def change_pol_degrees(degs: list[int]):
    AppState().pol_degrees = degs


def change_dims(dims: list[int]):
    AppState().dims = dims


def change_optimizer(new_opt: str):
    AppState().opt = Optimizer.translate(new_opt).value
