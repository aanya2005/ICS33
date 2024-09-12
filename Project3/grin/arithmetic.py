from grin.exception_handling import GrinException
from grin import GrinTokenKind


class Arithmetics:
    """
    Handles arithmetic functionality.
    Takes in program from processing file.
    """
    def __init__(self, program):
        self.p = program

    def add(self, op1, op2):
        """Handles addition of two variables."""
        if type(self.p.variables[op1.text()]) is str:
            if type(op2.value()) is int or type(op2.value()) is float \
                    or (op2.kind() is GrinTokenKind.IDENTIFIER and type(self.p.variables[op2.text()]) is int) \
                    or (op2.kind() is GrinTokenKind.IDENTIFIER and type(self.p.variables[op2.text()]) is float):
                raise GrinException("can't add number and string", op1.location())
        else:
            if type(op2.value()) is str or \
                    type(self.p.variables[op2.text()]) is str:
                raise GrinException("can't add number and string", op1.location())

        if op2.kind() == GrinTokenKind.IDENTIFIER:
            self.p.variables[op1.text()] += self.p.variables[op2.text()]
        else:
            self.p.variables[op1.text()] += op2.value()


    def sub(self, op1, op2):
        """Handles subtraction of two variables."""
        if type(self.p.variables[op1.text()]) is str or \
                op2.value() is str or (
                op2.kind() == GrinTokenKind.IDENTIFIER and type(self.p.variables[op2.text()]) is str):
            raise GrinException("can't subtract string", op1.location())

        if op2.kind() == GrinTokenKind.IDENTIFIER:
            self.p.variables[op1.text()] -= self.p.variables[op2.text()]
        else:
            self.p.variables[op1.text()] -= op2.value()


    def mult(self, op1, op2):
        """Handles multiplication of two variables."""
        try:
            if op2.kind() == GrinTokenKind.IDENTIFIER:
                self.p.variables[op1.text()] *= self.p.variables[op2.text()]
            else:
                self.p.variables[op1.text()] *= op2.value()
        except TypeError:
            raise GrinException("can't multiply two strings", op1.location())


    def div(self, op1, op2):
        """Handles division of two variables."""
        if type(self.p.variables[op1.text()]) is str or \
                type(op2.value()) is str or (
                op2.kind() == GrinTokenKind.IDENTIFIER and type(self.p.variables[op2.text()]) is str):
            raise GrinException("can't divide string", op1.location())

        if op2.value() == 0 or (
                op2.kind() == GrinTokenKind.IDENTIFIER and self.p.variables[op2.text()] == 0):
            raise GrinException("zero operand", op1.location())

        if op2.kind() == GrinTokenKind.IDENTIFIER:
            if type(self.p.variables[op2.text()]) is int and type(self.p.variables[op1.text()]) is int:
                self.p.variables[op1.text()] //= self.p.variables[op2.text()]
            else:
                self.p.variables[op1.text()] /= self.p.variables[op2.text()]
        else:
            if type(op2.value()) is int and type(self.p.variables[op1.text()]) is int:
                self.p.variables[op1.text()] //= op2.value()
            else:
                self.p.variables[op1.text()] /= op2.value()