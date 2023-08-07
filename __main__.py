import os
import sys
import warnings

ROOT = os.path.abspath(os.path.join(__file__, ".."))
sys.path.insert(1, ROOT)


from event import init_app_event
from tools.config import LOGO_PATH
from views import App

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    app = App()
    app.iconbitmap(LOGO_PATH)
    init_app_event(app)
    app.mainloop()
