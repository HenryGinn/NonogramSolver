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

    def update_grid_discluded(self, updating_indexes):
        self.nonogram.grid_discluded[updating_indexes, self.index] = True
