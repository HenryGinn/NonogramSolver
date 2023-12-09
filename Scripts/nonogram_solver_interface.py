from nonogram import Nonogram

my_nonogram = Nonogram("GCHQ.json", window_size="full",
                       colour="psycho", show_lines=False,
                       show_discluded=False)
my_nonogram.solve()
