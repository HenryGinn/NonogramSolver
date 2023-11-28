import math

import numpy as np

from hgutilities import defaults

class Grid():

    def __init__(self, display):
        self.display = display
        self.inherit_from_display()

    def inherit_from_display(self):
        attributes = ["nonogram", "window", "canvas",
                      "window_height", "window_width",
                      "grid_buffer", "foreground_colour"]
        defaults.inherit(self, self.display, attributes)

    def draw_grid(self):
        self.set_grid_parameters()
        self.draw_thin_lines()

    def set_grid_parameters(self):
        self.grid_size = self.window_height - 2 * self.grid_buffer
        self.cell_size = self.grid_size / self.nonogram.size
        self.left_edge = (self.window_width - self.grid_size) / 2
        self.right_edge = self.left_edge + self.grid_size
        self.top_edge = self.grid_buffer
        self.bottom_edge = self.top_edge + self.grid_size
    
    def draw_thin_lines(self):
        self.draw_thin_lines_horizontal()
        self.draw_thin_lines_vertical()

    def draw_thin_lines_horizontal(self):
        line_positions = np.arange(self.nonogram.size + 1)
        for line_position in line_positions:
            y_position = self.top_edge + line_position * self.cell_size
            self.draw_thin_horizontal_line(y_position)

    def draw_thin_horizontal_line(self, y_position):
        self.canvas.create_line(self.left_edge, y_position,
                                self.right_edge, y_position,
                                fill=self.foreground_colour)

    def draw_thin_lines_vertical(self):
        line_positions = np.arange(self.nonogram.size + 1)
        for line_position in line_positions:
            x_position = self.left_edge + line_position * self.cell_size
            self.draw_thin_vertical_line(x_position)

    def draw_thin_vertical_line(self, x_position):
        self.canvas.create_line(x_position, self.top_edge,
                                x_position, self.bottom_edge,
                                fill=self.foreground_colour)
