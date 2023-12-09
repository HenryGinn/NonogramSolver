import tkinter as tk
from itertools import accumulate

from hgutilities import defaults
import numpy as np

class Grid():

    def __init__(self, display):
        self.display = display
        self.nonogram = display.nonogram
        self.canvas = display.canvas
        self.inherit_window_parameters()

    def inherit_window_parameters(self):
        self.window_width = self.display.window_width
        self.window_height = self.display.window_height
        self.window_buffer_x = round(self.window_width * self.display.window_buffer_x_ratio)
        self.window_buffer_y = round(self.window_height * self.display.window_buffer_y_ratio)

    def draw_grid_and_labels(self):
        self.set_label_lengths()
        self.set_grid_size_constants()
        self.draw_labels()
        self.draw_grid()

    def set_label_lengths(self):
        self.vertical_label_length = max([len(label) for label in self.nonogram.column_data])
        self.horizontal_label_length = max([len(label) for label in self.nonogram.row_data])

    def set_grid_size_constants(self):
        self.set_label_lengths()
        self.set_cell_size()
        self.set_display_sizes()
        self.set_grid_reference_coordinates()
        self.set_grid_ends()

    def set_cell_size(self):
        cell_width = self.get_potential_cell_width()
        cell_height = self.get_potential_cell_height()
        self.set_slack_direction_from_cell_dimensions(cell_width, cell_height)
        self.cell_size = int(min(cell_width, cell_height))
        self.set_font_kwargs()

    def get_potential_cell_width(self):
        allocated_width = self.window_width - 2*self.window_buffer_x
        numerator = allocated_width * self.font_height_width_ratio
        denominator = self.nonogram.width*self.font_height_width_ratio + self.horizontal_label_length*self.display.text_ratio
        cell_width = numerator / denominator
        return cell_width

    def get_potential_cell_height(self):
        allocated_height = self.window_height - 2*self.window_buffer_y
        numerator = allocated_height * self.font_height_width_ratio
        denominator = self.nonogram.height*self.font_height_width_ratio + self.vertical_label_length * self.font_height_width_ratio
        cell_height = numerator / denominator
        return cell_height

    def set_slack_direction_from_cell_dimensions(self, cell_width, cell_height):
        if cell_width >= cell_height:
            self.slack_direction = "Horizontal"
        else:
            self.slack_direction = "Vertical"

    def set_font_kwargs(self):
        self.display.font_size = round(3 * self.display.text_ratio * self.cell_size / 4)
        self.display.font_kwargs = {"font": (self.display.font_style, self.display.font_size),
                                    "fill": self.display.colour}

    def set_display_sizes(self):
        self.set_grid_dimensions()
        self.set_label_sizes()

    def set_grid_dimensions(self):
        self.grid_width = self.nonogram.width * self.cell_size
        self.grid_height = self.nonogram.height * self.cell_size

    def set_label_sizes(self):
        self.labels_width = self.cell_size * self.display.text_ratio * self.horizontal_label_length / self.font_height_width_ratio
        self.labels_height = self.cell_size * self.vertical_label_length

    def set_grid_reference_coordinates(self):
        if self.slack_direction == "Horizontal":
            self.set_grid_reference_coordinates_horizontal()
        else:
            self.set_grid_reference_coordinates_vertical()

    def set_grid_reference_coordinates_horizontal(self):
        self.grid_reference_x = int((self.window_width + self.labels_width - self.grid_width)/2)
        self.grid_reference_y = self.window_buffer_y + self.labels_height

    def set_grid_reference_coordinates_vertical(self):
        self.grid_reference_x = self.window_buffer_x + self.labels_width
        self.grid_reference_y = int((self.window_height + self.labels_height - self.grid_height)/2)

    def set_grid_ends(self):
        self.x_end = self.grid_reference_x + self.grid_width
        self.y_end = self.grid_reference_y + self.grid_height


    def draw_labels(self):
        self.draw_row_labels()
        self.draw_column_labels()

    def draw_row_labels(self):
        for row_index, label in enumerate(self.nonogram.row_data):
            label = "  ".join([str(number) for number in label])
            self.draw_row_label(row_index, label)

    def draw_row_label(self, index, label):
        x_position = self.grid_reference_x - int(self.cell_size / 2)
        y_position = self.grid_reference_y + int((index + 1/2) * self.cell_size)
        self.canvas.create_text(x_position, y_position, text=label,
                                anchor="e", **self.display.font_kwargs)

    def draw_column_labels(self):
        for column_index, label_set in enumerate(self.nonogram.column_data):
            for index, label in enumerate(label_set):
                inverted_index = len(label_set) - index - 1
                self.draw_column_label(column_index, inverted_index, label)

    def draw_column_label(self, column_index, index, label):
        x_offset = len(str(label)) * 1/2 * self.display.font_size * self.display.text_ratio
        x_position = self.grid_reference_x + int((column_index + 1/2) * self.cell_size - x_offset)
        y_position = self.grid_reference_y - int((index + 1/2) * self.cell_size)
        self.canvas.create_text(x_position, y_position, text=label,
                                anchor="w", **self.display.font_kwargs)

    def draw_grid(self):
        if self.display.show_lines:
            self.draw_vertical_lines()
            self.draw_horizontal_lines()

    def draw_vertical_lines(self):
        for column_index in range(self.nonogram.width + 1):
            x_position = self.grid_reference_x + int(column_index * self.cell_size)
            self.draw_vertical_line(x_position)

    def draw_vertical_line(self, x_position):
        self.canvas.create_line(x_position, self.grid_reference_y,
                                x_position, self.y_end,
                                fill=self.display.colour,
                                width=self.display.line_width)

    def draw_horizontal_lines(self):
        for row_index in range(self.nonogram.height + 1):
            y_position = self.grid_reference_y + int(row_index * self.cell_size)
            self.draw_horizontal_line(y_position)

    def draw_horizontal_line(self, y_position):
        self.canvas.create_line(self.grid_reference_x, y_position,
                                self.x_end, y_position,
                                fill=self.display.colour,
                                width=self.display.line_width)

    def set_cells_corners(self):
        self.set_cells_corners_1()
        self.set_cells_corners_2()

    def set_cells_corners_1(self):
        self.cells_corners_1 = [[self.get_cell_corners_1(x, y)
                                 for x in range(self.nonogram.width)]
                                for y in range(self.nonogram.height)]

    def set_cells_corners_2(self):
        self.cells_corners_2 = [[self.get_cell_corners_2(x, y)
                                 for x in range(self.nonogram.width)]
                                for y in range(self.nonogram.height)]

    def get_cell_corners_1(self, x, y):
        top_left_x = self.grid_reference_x + x * self.cell_size
        top_left_y = self.grid_reference_y + y * self.cell_size
        bottom_right_x = self.grid_reference_x + (x+1) * self.cell_size
        bottom_right_y = self.grid_reference_y + (y+1) * self.cell_size
        return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)

    def get_cell_corners_2(self, x, y):
        top_right_x = self.grid_reference_x + (x+1) * self.cell_size
        top_right_y = self.grid_reference_y + y * self.cell_size
        bottom_left_x = self.grid_reference_x + x * self.cell_size
        bottom_left_y = self.grid_reference_y + (y+1) * self.cell_size
        return (top_right_x, top_right_y, bottom_left_x, bottom_left_y)

    def include_cell(self, x, y):
        cell_corners = self.cells_corners_1[x][y]
        self.canvas.create_rectangle(*cell_corners,
                                     fill=self.display.colour,
                                     outline=self.display.colour)

    def disclude_cell(self, x, y):
        if self.display.show_discluded:
            self.draw_cross_positive(x, y)
            self.draw_cross_negative(x, y)

    def draw_cross_positive(self, x, y):
        cell_corners = self.cells_corners_1[x][y]
        self.canvas.create_line(*cell_corners,
                                fill=self.display.colour,
                                width=self.display.line_width)

    def draw_cross_negative(self, x, y):
        cell_corners = self.cells_corners_2[x][y]
        self.canvas.create_line(*cell_corners,
                                fill=self.display.colour,
                                width=self.display.line_width)

defaults.load(Grid)
