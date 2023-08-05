import tkinter as tk
import tkinter.ttk as ttk


class Splash(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lift()
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        self.title("ctpros")
        self.label = ttk.Label(
            self, text="Initializing and checking for updates... Please wait."
        )
        self.label.pack(padx=25, pady=25)
        self.update_idletasks()


splash = Splash()


import lazy_import

for module in [
    "mayavi",
    "pandas",
    "scipy.linalg",
    "scipy.ndimage",
    "scipy.optimize",
    "scipy.stats",
    "scipy.signal",
    "skimage.measure",
    "skimage.morphology",
    "scipy",
    "skimage",
    "vtk",
]:
    lazy_import.lazy_module(module)


import sys


def main(argv):
    from ctpros.graphics import GUI, Updater
    from ctpros.graphics.components.tools import check_updates

    update = check_updates()
    if update is not None and "win" in sys.platform:
        Updater(*update).mainloop()
    splash.destroy()
    gui = GUI(*argv)
    gui.mainloop()


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
