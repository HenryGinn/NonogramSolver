import sys
import os
import json
import time

from hgutilities import defaults
import numpy as np

from user_nonogram import UserNonogram
from display.display import Display
from row import Row
from column import Column


class Nonogram():

    def __init__(self, *args, **kwargs):
        self.args_and_kwargs(*args, **kwargs)
        self.set_paths()
        self.set_problem()
        self.draw()

    def args_and_kwargs(self, *args, **kwargs):
        self.process_args(args)
        self.kwargs = kwargs
        defaults.kwargs(self, **kwargs)

    def process_args(self, args):
        if len(args) == 1:
            self.path_input = args[0]

    def set_paths(self):
        script_path = sys.path[0]
        repository_path = os.path.split(script_path)[0]
        self.problems_path = os.path.join(repository_path, "Puzzles")

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
        self.set_grid_included()
        self.grid_discluded = np.ones((self.width, self.height)) * False

    def set_grid_included(self):
        self.grid_included = np.ones((self.width, self.height)) * False
        if len(self.problem_dict["Existing cells included"]) != 0:
            self.add_existing_included_cells()

    def add_existing_included_cells(self):
        included_x, included_y = zip(*self.problem_dict["Existing cells included"])
        included_x, included_y = np.array(included_x), np.array(included_y)
        self.grid_included[included_x, included_y] = True

    def set_line_data(self):
        self.row_data = self.problem_dict["Row data"]
        self.column_data = self.problem_dict["Column data"]

    def draw(self):
        self.display_obj = Display(self)
        self.display_obj.display(self.kwargs)

    def update_display(self):
        self.display_obj.update()

    def solve(self):
        self.initialise()
        while self.continue_iterating:
            self.iterate()

    def initialise(self):
        self.initialise_iteration_variables()
        self.rows, self.columns = [], []
        self.initialise_rows()
        self.initialise_columns()

    def initialise_iteration_variables(self):
        self.continue_iterating = True
        self.changes_made = False
        
    def initialise_rows(self):
        for row_index, data in enumerate(self.row_data):
            row = Row(self, row_index, data)
            self.rows.append(row)

    def initialise_columns(self):
        for column_index, data in enumerate(self.column_data):
            column = Column(self, column_index, data)
            self.columns.append(column)

    def iterate(self):
        self.continue_iterating = False
        self.update_lines(self.rows)
        self.update_lines(self.columns)

    def update_lines(self, lines):
        for line in lines:
            line.update()
            self.update_output_if_necessary()

    def update_output_if_necessary(self):
        if self.changes_made:
            self.changes_made = False
            self.continue_iterating = True
            self.update_display()
        

defaults.load(Nonogram)
