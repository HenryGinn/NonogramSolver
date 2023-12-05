from line import Line

class Column(Line):

    def __init__(self, nonogram, index, data):
        self.direction = "Column"
        self.total_length = nonogram.height
        Line.__init__(self, nonogram, index, data)
