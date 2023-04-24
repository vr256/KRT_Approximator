import customtkinter

from menu import Sidebar, YSelector, YCalculator, MainTabview, \
                 SystemSolver, VectorView, PolynomView, AdditionalView, \
                 InputView
from event import init_app_event

customtkinter.set_appearance_mode("Light") 
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # window
        self.title("СА Лабораторна робота №2")
        self.geometry(f"{1400}x{600}")

        # grid layout
        self.grid_columnconfigure((1, 2), weight=30)
        self.grid_columnconfigure(3, weight=20)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # contents
        self.sidebar = Sidebar(master=self, width=140, corner_radius=0)
        self.y_selector = YSelector(master=self)
        self.calculate_y = YCalculator(master=self)
        self.main_tabview = MainTabview(master=self, width=450)
        self.system_solver = SystemSolver(master=self)
        self.vector_view = VectorView(master=self, label_text="Вектори", width=95)
        self.polynom_view = PolynomView(master=self, label_text="Поліноми", width=95)  
        self.additional_view = AdditionalView(master=self, label_text="Додатково", width=150)
        self.input_view = InputView(master=self, label_text="Введення даних")


# Track computation time (evolutional algorithms)
# error warnings
# working file output and manual input

if __name__ == "__main__":
    app = App()
    init_app_event(app)
    app.mainloop()