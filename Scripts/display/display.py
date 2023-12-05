import tkinter as tk
import numpy as np

from display.display_settings import DisplaySettings
from display.grid import Grid

class Display():

    def __init__(self, nonogram):
        self.nonogram = nonogram
        self.window_initialised = False
        self.set_undrawn_cells()

    def display(self, kwargs):
        self.initialise_window(kwargs)

    def initialise_window(self, kwargs):
        if not self.window_initialised:
            self.do_initialise_window(kwargs)
            self.window_initialised = True

    def do_initialise_window(self, kwargs):
        self.process_kwargs(kwargs)
        self.create_window()
        self.draw_grid_and_labels()

    def process_kwargs(self, kwargs):
        display_settings = DisplaySettings(self)
        display_settings.process_kwargs(kwargs)
    
    def create_window(self):
        self.root = tk.Tk()
        self.set_window_sizes()
        self.setup_window()
        self.setup_canvas()

    def setup_window(self):
        self.root.title("Nonogram Solver")
        self.root.geometry(f"{self.window_width}x{self.window_height}-0+0")

    def set_window_sizes(self):
        self.window_width = int(self.root.winfo_screenwidth() * self.window_width_multiplier)
        self.window_height = int((self.root.winfo_screenheight() - 63) * self.window_height_multiplier)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.configure(bg=self.background_colour)
        self.canvas.pack()
        
    def draw_grid_and_labels(self):
        self.grid = Grid(self)
        self.grid.draw_grid_and_labels()
        self.grid.set_cells_corners()

    def set_undrawn_cells(self):
        self.undrawn_cells = np.ones((self.nonogram.width,
                                      self.nonogram.height)
                                     ) * True


    def update(self):
        self.update_inclusion()
        self.update_disclusion()

    def update_inclusion(self):
        cells_to_include = self.get_cells_to_include()
        for x, y in zip(*cells_to_include):
            self.undrawn_cells[x, y] = False
            self.grid.include_cell(x, y)

    def get_cells_to_include(self):
        undrawn_to_include = np.logical_and(self.undrawn_cells,
                                            self.nonogram.grid_included)
        cells_to_include = np.where(undrawn_to_include)
        return cells_to_include

    def update_disclusion(self):
        cells_to_disclude = self.get_cells_to_disclude()
        for x, y in zip(*cells_to_disclude):
            self.undrawn_cells[x, y] = False
            self.grid.disclude_cell(x, y)

    def get_cells_to_disclude(self):
        undrawn_to_disclude = np.logical_and(self.undrawn_cells,
                                             self.nonogram.grid_discluded)
        cells_to_disclude = np.where(undrawn_to_disclude)
        return cells_to_disclude
