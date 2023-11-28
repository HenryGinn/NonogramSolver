import sys
import os
import json

from hgutilities import defaults

from user_nonogram import UserNonogram
from puzzle import Puzzle
from display.display import Display


class Nonogram():

    def __init__(self, *args, **kwargs):
        self.args_and_kwargs(*args, **kwargs)
        self.puzzle = Puzzle(self)
        self.set_puzzle()
        self.draw()

    def args_and_kwargs(self, *args, **kwargs):
        self.process_args(args)
        self.kwargs = kwargs
        defaults.kwargs(self, **kwargs)

    def process_args(self, args):
        if len(args) == 1:
            self.path_input = args[0]

    def set_puzzle(self):
        self.data_file_input()
        self.set_puzzle_from_path()

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
        self.puzzles_path = os.path.join(repository_path, "Puzzles")
        self.path = os.path.join(self.puzzles_path, self.path_input)
        self.verify_valid_path()

    def verify_valid_path(self):
        if not os.path.exists(self.path):
            raise ValueError(f"Path cannot be found\n"
                             f"Input: {self.path_input}\n"
                             f"Path: {self.path}")

    def create_data_file_from_user(self):
        user_input_obj = UserNonogram(self)
        self.path = user_input_obj.path
        self.set_puzzle_from_path()

    def set_puzzle_from_path(self):
        self.set_puzzle_dict_from_path()
        self.set_dimensions()
        self.set_line_data()

    def set_puzzle_dict_from_path(self):
        with open(self.path, "r") as file:
            self.puzzle_dict = json.load(file)

    def set_dimensions(self):
        dimensions = self.puzzle_dict["Dimensions"]
        self.width = dimensions["Width"]
        self.height = dimensions["Height"]
        self.size = max(self.width, self.height)

    def set_line_data(self):
        self.row_data = self.puzzle_dict["Row data"]
        self.column_data = self.puzzle_dict["Column data"]

    def draw(self):
        self.display_obj = Display(self)
        self.display_obj.draw_grid()

defaults.load(Nonogram)
