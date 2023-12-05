from line import Line

class Row(Line):

    def __init__(self, nonogram, index, data):
        self.direction = "Row"
        self.total_length = nonogram.width
        Line.__init__(self, nonogram, index, data)

    def get_grid_line_included(self):
        grid_line_included = self.nonogram.grid_included[self.index, :]
        return grid_line_included

    def get_grid_line_discluded(self):
        grid_line_discluded = self.nonogram.grid_discluded[self.index, :]
        return grid_line_discluded

    def update_grid_included(self, updating_indexes):
        self.nonogram.grid_included[self.index, updating_indexes] = True

    def update_grid_discluded(self, updating_indexes):
        self.nonogram.grid_discluded[self.index, updating_indexes] = True
