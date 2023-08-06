import os
import sys
import warnings

ROOT = os.path.abspath(os.path.join(__file__, ".."))
sys.path.insert(1, ROOT)


from app import App
from event import init_app_event

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    app = App()
    app.iconbitmap("image/logo.ico")
    init_app_event(app)
    app.mainloop()
