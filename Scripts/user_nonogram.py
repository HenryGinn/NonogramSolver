class UserNonogram():

    def __init__(self, nonogram_obj):
        self. nonogram_obj = nonogram_obj
        self.set_path()
        self.set_puzzle_dimensions()
        self.set_puzzle_data()

    def set_path(self):
        file_name = get_file_name()
        self.path = os.path.join(self.nonogram_obj.puzzles_path, file_name)

    def set_puzzle_dimensions(self):
        self.set_width()
        self.set_height()

    def set_width(self):
        prompt = "Please enter the width of the puzzle:\n"
        self.width = get_int(prompt, lower_bound=0)

    def set_height(self):
        prompt = "Please enter the height of the puzzle:\n"
        self.height = get_int(prompt, lower_bound=0)

    def set_puzzle_data(self):
        self.set_puzzle_data_horizontal()
        self.set_puzzle_data_vertical()
        self.add_existing_data()

    def set_puzzle_data_horizontal(self):
        print(("\nPlease enter the data for the columns\n"
               "Use spaces as a delimiter\n"))
        self.horizontal_data = [self.get_line_data("column", column_index)
                                for column_index in range(self.width)]

    def set_puzzle_data_vertical(self):
        print(("\nPlease enter the data for the rows\n"
               "Use spaces as a delimiter\n"))
        self.vertical_data = [self.get_line_data("row", row_index)
                                for row_index in range(self.width)]

    def get_line_data(self, line_type, index):
        pass

    def add_existing_data(self):
        pass
