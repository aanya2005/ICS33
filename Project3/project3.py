# project3.py
#
# ICS 33 Spring 2024
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

import grin
from grin.processing import Running
from grin import GrinTokenKind


def _read_input():
    """Reads the input from the standard input."""
    program = Running()
    while True:
        statement = input()
        if statement.strip() == '.':
            break
        program.add_command(statement)
    program.preprocess()
    while program.runnable():
        line = program.get_statement()
        _process_statement(program, line)

def _process_statement(program, line):
    """Processes a single statement based on its keyword kind."""
    # Not tested as these do not have the required returnable functions.
    keyword_kind = line[0].kind()
    if keyword_kind in (GrinTokenKind.INSTR, GrinTokenKind.INNUM, GrinTokenKind.PRINT):
        program.io(keyword_kind, line[1])
        program.forward()
    elif keyword_kind in (GrinTokenKind.ADD, GrinTokenKind.SUB, GrinTokenKind.MULT,
                          GrinTokenKind.DIV, GrinTokenKind.LET):
        program.op(keyword_kind, line[1], line[2])
        program.forward()
    elif keyword_kind == grin.GrinTokenKind.END:
        program.end()
    elif keyword_kind in (GrinTokenKind.GOTO, GrinTokenKind.GOSUB):
        program.jump(keyword_kind, line[1], line[0].location()) \
            if len(line) < 3 or program.eval(line[3], line[4].kind(), line[5],
                                             line[4].location()) \
            else program.forward()
    elif keyword_kind == GrinTokenKind.RETURN:
        program.backtrack()

def main() -> None:
    """Runs the simulation program in its entirety."""
    _read_input() # Not tested as this has no returnable function.


if __name__ == '__main__':
    main()
