import tkinter as tk
from hgutilities import defaults

from .grid import Grid

class Display():

    def __init__(self, nonogram):
        defaults.kwargs(self, nonogram.kwargs)
        self.nonogram = nonogram
        self.process_display_settings()
        self.create_window()

    def process_display_settings(self):
        self.set_window_multipliers()
        self.set_colours()

    def set_window_multipliers(self):
        window_multipliers_dict = self.get_window_multiplers_dict()
        multipliers = window_multipliers_dict[self.window]
        self.window_width_multiplier = multipliers[0]
        self.window_height_multiplier = multipliers[1]

    def get_window_multiplers_dict(self):
        multipliers_dict = {"full": (1, 1),
                            "half": (0.5, 1),
                            "quarter": (0.5, 0.5)}
        return multipliers_dict

    def set_colours(self):
        self.background_colour = self.dark_background_colour
        self.foreground_colour = self.dark_foreground_colour

    def create_window(self):
        self.root = tk.Tk()
        self.set_window_sizes()
        self.setup_window()
        self.setup_canvas()

    def set_window_sizes(self):
        self.window_width = int(self.root.winfo_screenwidth() * self.window_width_multiplier)
        self.window_height = int((self.root.winfo_screenheight() - 65) * self.window_height_multiplier)

    def setup_window(self):
        self.root.title("Nonogram Solver")
        self.root.geometry(f"{self.window_width}x{self.window_height}-0+0")

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.configure(bg=self.background_colour)
        self.canvas.pack()

    def draw_grid(self):
        self.grid_obj = Grid(self)
        self.grid_obj.draw_grid()

    def initialise_grid_numbers(self):
        self.set_fonts()
        self.grid_obj.set_cell_positions()

    def set_fonts(self):
        self.font = {"font": ("Calibri", round(0.65*self.grid_obj.cell_size)),
                     "fill": self.foreground_colour}
        defaults.inherit(self.grid_obj, self, ["font"])

defaults.load(Display)
