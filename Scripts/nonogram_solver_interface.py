from nonogram import Nonogram

#my_nonogram = Nonogram("Puzzle 1.json")
#my_nonogram = Nonogram("Puzzle 2.json")
#my_nonogram = Nonogram("Puzzle 3.json")
my_nonogram = Nonogram("GCHQ.json", window_size="full", mode="psycho")
my_nonogram.update_display()
my_nonogram.solve()
