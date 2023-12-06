from line import Line

class Column(Line):

    def __init__(self, nonogram, index, data):
        self.direction = "Column"
        self.total_length = nonogram.height
        Line.__init__(self, nonogram, index, data)

    def get_grid_line_included(self):
        grid_line_included = self.nonogram.grid_included[:, self.index]
        return grid_line_included

    def get_grid_line_discluded(self):
        grid_line_discluded = self.nonogram.grid_discluded[:, self.index]
        return grid_line_discluded

    def update_grid_included(self, updating_indexes):
        self.nonogram.grid_included[updating_indexes, self.index] = True
        self.update_message(updating_indexes, "include")

    def update_grid_discluded(self, updating_indexes):
        self.nonogram.grid_discluded[updating_indexes, self.index] = True
        self.update_message(updating_indexes, "disclude")

    def update_message(self, indices, state):
        print(f"\nBy considering column {self.index + 1} we could "
              f"{state} the following cells:")
        for index in indices[0]:
            print(f"Row: {index + 1}    Column: {self.index + 1}")
