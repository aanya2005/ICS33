from grin.arithmetic import Arithmetics
from grin.exception_handling import GrinException
from collections import defaultdict
from grin import parse, GrinTokenKind
from grin.inputoutput import InputOutput


class Running(Arithmetics,InputOutput):
    """Runs the whole program and handles all functionality."""

    def __init__(self):
        super().__init__(self)
        self.program = []
        self.counter = 0
        self.functions = {}
        self.command = []
        self.stack = []
        self.variables = defaultdict(int)
        self.arith = Arithmetics(self)
        self.evalmodule = InputOutput(self)

    def add_command(self,statement):
        """Saves all the commands."""
        self.command.append(statement)

    def preprocess(self):
        """Parses and handles all commands."""
        self.program = list(parse(self.command))
        for i in range(len(self.program)):
            row = self.program[i]
            first_token = row[0]
            # Not tested because basic functionality already tested
            if first_token.kind() == GrinTokenKind.IDENTIFIER:
                self.functions[first_token.text()] = first_token.location().line() - 1
                self.program[i]= row[2:]

    def io(self,command, token):
        """Checks if command is input or output."""
        if command == GrinTokenKind.PRINT:
            self.evalmodule.output(token)
        # Cannot test else case as input must be taken
        else:
            val = input()
            self.evalmodule.input(command,token,val)

    def end(self):
        """Ends the program."""
        self.counter = len(self.program)

    def forward(self):
        """Takes the program to the next line."""
        self.counter +=1

    def runnable(self):
        """Checks if program end line has been reached."""
        return self.counter < len(self.program)

    def jump(self, keyword_kind, target, location):
        """Handles GOTO and GOSUB commands."""
        msg = 'GOTO' if keyword_kind == GrinTokenKind.GOTO else 'GOSUB'
        # GOSUB functions
        if keyword_kind == GrinTokenKind.GOSUB:
            if target.kind() == GrinTokenKind.LITERAL_INTEGER:
                if target.value() == 0 or target.value() + self.counter < 0 or target.value() + self.counter >= len(
                        self.program):
                    raise GrinException(f'invalid {msg} statement', location)

                self.stack.append(self.counter+1)
                self.counter = target.value() + self.counter
            # Not tested because both first cases are the same,
            # causing it to fall through the first one.
            elif target.kind() == GrinTokenKind.LITERAL_STRING:
                if self.functions.get(target.value()) is None:
                    raise GrinException(f'invalid {msg} statement', location)

                self.stack.append(self.counter + 1)
                self.counter = self.functions.get(target.value())
            # Newly added line of code
            elif target.kind() == GrinTokenKind.IDENTIFIER:
                if target.value() in self.variables:
                    if type(self.variables[target.value()]) is str:
                        self.counter =self.functions.get(self.variables[target.value()])
                    else:
                        self.counter = self.counter+ self.variables[target.value()]
            # Until here
            else:
                if self.functions.get(target.text()) is None:
                    raise GrinException(f'invalid {msg} statement', location)

                self.stack.append(self.counter + 1)
                self.counter = self.functions.get(target.text())

        # GOTO functions
        if keyword_kind == GrinTokenKind.GOTO:
            if target.kind() == GrinTokenKind.LITERAL_INTEGER:
                if target.value() == 0 or target.value() + self.counter < 0 or target.value() + self.counter >= len(self.program):
                    raise GrinException(f'invalid {msg} statement',location)

                self.counter = target.value() + self.counter
            # Not tested because both first ifs are the same,
            # causing it to fall through the first one while testing.
            elif target.kind() == GrinTokenKind.LITERAL_STRING:
                if self.functions.get(target.value()) is None:
                    raise GrinException(f'invalid {msg} statement',location)
                else:
                    self.counter = self.functions.get(target.value())
            # Newly added line of code
            elif target.kind() == GrinTokenKind.IDENTIFIER:
                target_line = target.value()
                if target_line in self.variables:
                    if type(self.variables[target_line]) is str:
                        self.counter =self.functions.get(self.variables[target_line])
                    else:
                        self.counter = self.counter+ self.variables[target_line]
            # Until here
            else:
                if self.functions.get(target.text()) is None:
                    raise GrinException(f'invalid {msg} statement',location)
                else:
                    self.counter = self.functions.get(target.text())

    def backtrack(self):
        """Handles returns."""
        if len(self.stack) > 0:
            self.counter = self.stack.pop()
        else:
            self.counter+=1
    # Tested in test_grin_processor

    def eval(self, op1, comp_kind, op2, location):
        """Handles the relational operations."""
        val1 = self.variables[op1.text()] if op1.kind() == GrinTokenKind.IDENTIFIER else op1.value()
        val2 = self.variables[op2.text()] if op2.kind() == GrinTokenKind.IDENTIFIER else op2.value()
        if (type(val1) is str and type(val2) is not str) or (
                type(val1) is not str and type(val2) is str):
            raise GrinException("invalid operands for comparison", location)

        if comp_kind == GrinTokenKind.LESS_THAN:
            return val1 < val2
        elif comp_kind == GrinTokenKind.LESS_THAN_OR_EQUAL:
            return val1 <= val2
        elif comp_kind == GrinTokenKind.GREATER_THAN:
            return val1 > val2
        elif comp_kind == GrinTokenKind.GREATER_THAN_OR_EQUAL:
            return val1 >= val2
        elif comp_kind == GrinTokenKind.EQUAL:
            return val1 == val2
        else:
            return val1 != val2
        # Tested completely in test_grin_processor


    def get_statement(self):
        """Returns the statements."""
        return self.program[self.counter]

    def op(self,kind,op1,op2):
        """Checks the kind of arithmetic operators."""
        if kind == GrinTokenKind.LET: # Tested in test_grin_processing
            self.let(op1,op2)
        elif kind == GrinTokenKind.ADD:
            self.arith.add(op1,op2)
        elif kind == GrinTokenKind.SUB:
            self.arith.sub(op1,op2)
        elif kind == GrinTokenKind.MULT:
            self.arith.mult(op1,op2)
        else:
            self.arith.div(op1,op2)
        # All arithmetic ones tested by test_grin_arithmetic

    def let(self,op1,op2):
        """Handles saving of variables."""
        if op2.kind() == GrinTokenKind.IDENTIFIER:
            self.variables[op1.text()] = self.variables[op2.text()]
        else:
            self.variables[op1.text()] = op2.value()
        # tested by test_grin_processor
