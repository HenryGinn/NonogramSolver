import numpy as np

class Collection():

    def __init__(self, line, gaps):
        self.process_inputs(line, gaps)
        self.set_real_gaps()
        self.cells = np.zeros(self.line.total_length) * False
        self.populate_cells()

    def process_inputs(self, line, gaps):
        self.line = line
        self.gaps = gaps

    def set_real_gaps(self):
        for index in range(1, len(self.gaps) - 1):
            self.gaps[index] += 1

    def populate_cells(self):
        starts = self.get_starts()
        for start, length in zip(starts, self.line.data):
            end = start + length
            self.cells[start:end] = True

    def get_starts(self):
        cumulative_gaps = self.line.get_cumulative(self.gaps)
        later_starts = [gap + contiguous
                        for gap, contiguous in zip(cumulative_gaps[1:],
                                                   self.line.cumulative_contiguous)]
        starts = [self.gaps[0]] + later_starts
        return starts
