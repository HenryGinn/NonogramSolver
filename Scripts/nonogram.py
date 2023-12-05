import sys
import os
import json

from hgutilities import defaults
import numpy as np

from user_nonogram import UserNonogram
from problem import Problem
from display.display import Display
from row import Row
from column import Column


class Nonogram():

    def __init__(self, *args, **kwargs):
        self.args_and_kwargs(*args, **kwargs)
        self.problem = Problem(self)
        self.set_problem()
        self.draw()

    def args_and_kwargs(self, *args, **kwargs):
        self.process_args(args)
        self.kwargs = kwargs
        defaults.kwargs(self, **kwargs)

    def process_args(self, args):
        if len(args) == 1:
            self.path_input = args[0]

    def set_problem(self):
        self.data_file_input()
        self.set_problem_from_path()

    def data_file_input(self):
        if hasattr(self, "path_input"):
            self.set_path_from_path_input()
        else:
            self.create_data_file_from_user()

    def set_path_from_path_input(self):
        if os.path.exists(self.path_input):
            self.path = self.path_input
        else:
            self.set_path_from_file_name()

    def set_path_from_file_name(self):
        script_path = sys.path[0]
        repository_path = os.path.split(script_path)[0]
        self.problems_path = os.path.join(repository_path, "Puzzles")
        self.path = os.path.join(self.problems_path, self.path_input)
        self.verify_valid_path()

    def verify_valid_path(self):
        if not os.path.exists(self.path):
            raise ValueError(f"Path cannot be found\n"
                             f"Input: {self.path_input}\n"
                             f"Path: {self.path}")

    def create_data_file_from_user(self):
        user_input_obj = UserNonogram(self)
        self.path = user_input_obj.path
        self.set_problem_from_path()

    def set_problem_from_path(self):
        self.set_problem_dict_from_path()
        self.set_dimensions()
        self.set_grid_data()
        self.set_line_data()

    def set_problem_dict_from_path(self):
        with open(self.path, "r") as file:
            self.problem_dict = json.load(file)

    def set_dimensions(self):
        dimensions = self.problem_dict["Dimensions"]
        self.width = dimensions["Width"]
        self.height = dimensions["Height"]
        self.size = max(self.width, self.height)

    def set_grid_data(self):
        self.grid_included = np.ones((self.width, self.height)) * False
        self.grid_discluded = np.ones((self.width, self.height)) * False

    def set_line_data(self):
        self.row_data = self.problem_dict["Row data"]
        self.column_data = self.problem_dict["Column data"]

    def draw(self):
        self.display_obj = Display(self)
        self.display_obj.display(self.kwargs)

    def update_display(self):
        self.display_obj.update()

    def solve(self):
        self.iterate()
        self.update_display()

    def iterate(self):
        self.rows, self.columns = [], []
        self.initialise_rows()
        self.initialise_columns()
        
    def initialise_rows(self):
        for row_index, data in enumerate(self.row_data):
            row = Row(self, row_index, data)
            self.rows.append(row)
        self.update_lines(self.rows)

    def initialise_columns(self):
        for row_index, data in enumerate(self.row_data):
            column = Column(self, row_index, data)
            self.columns.append(column)
        self.update_lines(self.columns)

    def update_lines(self, lines):
        for line in lines:
            line.update()


defaults.load(Nonogram)
