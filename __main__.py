import os
import sys
import warnings

ROOT = os.path.abspath(os.path.join(__file__, ".."))
sys.path.insert(1, ROOT)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from tools.config import LOGO_PATH
from views import App

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    app = App()
    app.iconbitmap(LOGO_PATH)
    app.mainloop()
