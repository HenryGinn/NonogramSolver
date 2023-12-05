from hgutilities import defaults

class SlackSolve():

    def __init__(self, nonogram):
        self.inherit_from_nonogram(nonogram)

    def inherit_from_nonogram(self, nonogram):
        self.nonogram = nonogram
        kwargs = [""]
        defaults.inherit(self, nonogram, kwargs)
