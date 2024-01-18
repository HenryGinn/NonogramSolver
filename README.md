# NonogramSolver
A program to solve nonograms

## Basic Information

For a demonstration of what the program does, run the `nonogram_solver_interface` script. This will run the GCHQ 2015 Christmas puzzle (additional formatting kwargs have been passed in to match the intended output format).

This program is controlled from the `nonogram_solver_interface` script. Each nonogram puzzle is stored in a json file in the Puzzles folder, and these can be loaded in or created. A `Nonogram` object is created and a file name is passed in. If this file exists then it will be loaded, otherwise data about the puzzle will be asked and inputted by the user.

## Installing hgutilities

The package `hgutilities` is needed for this and can be installed with one of the following commands:
- (Windows and Debian based) pip install hgutilities
- (Windows) py3 -m pip install hgutilities
- (Windows) py -m pip install hgutilities
- (Debian based) python3 -m pip install hgutilities
- (Debian based) python -m pip install hgutilities

## Shortcomings and Things to do

- The size of the display is defined relative to the screen size, although currently it does not take into account the taskbar. Currently a hardcoded value has been subtracted from the height and it will not be consistent accross operating systems or with different taskbar positions.
- Currently only one technique has been implemented and this is not sufficient to solve all nonograms (for example, load "Puzzle 2.json"). An additional technique using more advanced logic or a recursive guess and check algorithm is necessary.
