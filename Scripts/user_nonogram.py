import os
import json

from int_input import get_int_input

class UserNonogram():

    def __init__(self, nonogram_obj):
        self. nonogram_obj = nonogram_obj
        self.set_path()
        self.set_puzzle_dimensions()
        self.set_puzzle_data()
        self.save_puzzle_data()

    def set_path(self):
        file_name = self.get_file_name()
        self.path = os.path.join(self.nonogram_obj.problems_path, file_name)

    def get_file_name(self):
        prompt = "Please enter a file name: "
        file_name = f"{input(prompt)}.json"
        return file_name

    def set_puzzle_dimensions(self):
        self.set_width()
        self.set_height()

    def set_width(self):
        prompt = "Please enter the width of the puzzle:\n"
        self.width = get_int_input(prompt, lower_bound=0)

    def set_height(self):
        prompt = "Please enter the height of the puzzle:\n"
        self.height = get_int_input(prompt, lower_bound=0)

    def set_puzzle_data(self):
        self.set_puzzle_data_horizontal()
        self.set_puzzle_data_vertical()
        self.add_existing_cells()

    def set_puzzle_data_horizontal(self):
        print(("\nPlease enter the data for the columns\n"
               "Use spaces as a delimiter\n"))
        self.horizontal_data = [self.get_line_data("Column", column_index)
                                for column_index in range(self.width)]

    def set_puzzle_data_vertical(self):
        print(("\nPlease enter the data for the rows\n"
               "Use spaces as a delimiter\n"))
        self.vertical_data = [self.get_line_data("Row", row_index)
                                for row_index in range(self.height)]

    def get_line_data(self, line_type, index):
        prompt = f"{line_type} {index + 1}: "
        while True:
            try:
                data_input = str(input(prompt))
                line_data = [int(number) for number in data_input.split(" ")]
                return line_data
            except:
                print("Fail, try again")

    def add_existing_cells(self):
        prompt = "Please enter how many cells are already included"
        existing_cell_count = get_int_input(prompt, lower_bound=0)
        self.existing_cells = [self.get_cell(cell_index)
                               for cell_index in range(existing_cell_count)]

    def get_cell(self, cell_index):
        prompt = f"Cell {cell_index + 1}: "
        while True:
            try:
                cell_input = str(input(prompt))
                cell = [int(number) - 1 for number in cell_input.split(" ")]
                return cell
            except:
                print("Fail, try again")

    def save_puzzle_data(self):
        self.construct_data_dict()
        with open(self.path, "w") as file:
            json.dump(self.data_dict, file, indent=2)

    def construct_data_dict(self):
        self.data_dict = {}
        self.collect_dimension_data()
        self.collect_line_data()
        self.collect_existing_cells()

    def collect_dimension_data(self):
        dimension_dict = {"Width": self.width,
                          "Height": self.height}
        self.data_dict.update({"Dimensions": dimension_dict})

    def collect_line_data(self):
        line_data = {"Row data": self.vertical_data,
                     "Column data": self.horizontal_data}
        self.data_dict.update(line_data)

    def collect_existing_cells(self):
        existing_cells = {"Existing cells included": self.existing_cells}
        self.data_dict.update(existing_cells)
