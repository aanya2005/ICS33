from grin import GrinTokenKind
from grin.exception_handling import GrinException

class InputOutput:
    """
    Handles i/o functionality.
    Takes in program from processing file.
    """
    def __init__(self, program):
        self.p = program

    def input(self, command, token, val):
        """Handles the inputs taken from INSTR."""
        if command == GrinTokenKind.INSTR:
            self.p.variables[token.value()] = val
        else:
            if '.' in val:
                try:
                    self.p.variables[token.value()] = float(val)
                except ValueError:
                    raise GrinException("invalid float in input", token.location())
            else:
                self.p.variables[token.value()] = int(val)


    def output(self, token):
        """Handles printing the outputs."""
        print(self.p.variables[token.value()]) if token.kind() == GrinTokenKind.IDENTIFIER else print(
            token.value())
