import os
import sys

ROOT = os.path.abspath(os.path.join(__file__, ".."))
sys.path.insert(1, ROOT)


from tools.config import LOGO_PATH
from views import App

if __name__ == "__main__":
    app = App()
    app.iconbitmap(LOGO_PATH)
    app.mainloop()
