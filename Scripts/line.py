"""
We reduce the problem to finding the different ways that non-negative
integers can add to a given total. These integers will correspond to
the sizes of the gaps but with some modifications to handle the
potential gaps of size 0 at the edges. The reason this will work is
because the total length of the contiguous sections is fixed, and this
implies the total length of the gaps is fixed. We will choose a total
so that there exists a bijection between sets of non-negative integers
that add to the total and valid lines.

We define the slack as the length of the line minus the length of the
contiguous sections. The modified slack is defined as the slack minus
the number of contiguous sections plus one. This is because each
contiguous section must be separated by the other contiguous sections
by at least one square and therefore the slack is reduced. The addition
of one is to account for an offset caused by the cause of a single
contiguous region that does not restrict the slack.
"""


import numpy as np

from collection import Collection

class Line():

    def __init__(self, nonogram, index, data):
        self.set_initial_variables(nonogram, index, data)
        self.set_line_properties()
        self.set_collections()

    def set_initial_variables(self, nonogram, index, data):
        self.nonogram = nonogram
        self.index = index
        self.data = data

    def set_line_properties(self):
        self.set_slack()
        self.cumulative_contiguous = self.get_cumulative(self.data)

    def set_slack(self):
        contiguous_length = sum(self.data)
        self.slack = self.total_length - contiguous_length - len(self.data) + 1

    def set_collections(self):
        self.collections = []
        self.populate_cells(len(self.data), self.slack, [])

    def get_cumulative(self, data):
        cumulative = [sum(data[:end_index + 1])
                      for end_index in range(len(data))]
        return cumulative

    def populate_cells(self, depth, remaining_slack, current_gaps):
        if depth > 0:
            self.iterate_over_remaining_slack(depth, remaining_slack, current_gaps)
        else:
            self.create_new_collection(remaining_slack, current_gaps)
        
    def iterate_over_remaining_slack(self, depth, remaining_slack, current_gaps):
        for gap_length in range(remaining_slack + 1):
            new_gaps = current_gaps + [gap_length]
            new_remaining_slack = remaining_slack - gap_length
            self.populate_cells(depth - 1, new_remaining_slack, new_gaps)

    def create_new_collection(self, remaining_slack, current_gaps):
        new_gaps = current_gaps + [remaining_slack]
        collection = Collection(self, new_gaps)
        self.collections.append(collection)

    def update(self):
        cells = np.stack([collection.cells for collection in self.collections])
        grid_line = self.get_grid_line()
        self.update_inclusion(cells, grid_line)
        self.update_disclusion(cells, grid_line)

    def update_inclusion(self, cells, grid_line):
        included = np.all(cells, axis=0)
        new_included = np.logical_xor(included, grid_line)
        updating_indexes_included = np.where(new_included)
        self.update_grid_included(updating_indexes_included)

    def update_disclusion(self, cells, grid_line):
        discluded = np.all(np.logical_not(cells), axis=0)
        new_discluded = np.logical_xor(discluded, grid_line)
        updating_indexes_discluded = np.where(new_discluded)
        self.update_grid_discluded(updating_indexes_discluded)
