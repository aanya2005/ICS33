import unittest
from io import StringIO
import sys
from project3 import _read_input
from grin.processing import Running
from grin import GrinTokenKind


class TestGrinFunctionality(unittest.TestCase):
    def test_outputs(self):
        input_lines = [
            'PRINT "HELLO"',
            '.'
        ]
        expected_output = "HELLO"
        original_input = sys.stdin
        sys.stdin = StringIO('\n'.join(input_lines))

        original_stdout = sys.stdout
        sys.stdout = StringIO()

        _read_input()

        actual_output = sys.stdout.getvalue().strip()
        sys.stdin = original_input
        sys.stdout = original_stdout
        self.assertEqual(actual_output, expected_output)

    def test_output_variables(self):
        input_lines = [
            'LET A 5',
            'PRINT A',
            '.'
        ]
        expected_output = "5"

        original_input = sys.stdin
        sys.stdin = StringIO('\n'.join(input_lines))

        original_stdout = sys.stdout
        sys.stdout = StringIO()

        _read_input()

        actual_output = sys.stdout.getvalue().strip()
        sys.stdin = original_input
        sys.stdout = original_stdout
        self.assertEqual(actual_output, expected_output)

    def test_input(self):
        run = Running()

        run.evalmodule.input(GrinTokenKind.INSTR, dummy_token,"123")
        self.assertEqual(run.variables["X"], '123')
        run.evalmodule.input(GrinTokenKind.INNUM, dummy_token, "123.0")
        self.assertEqual(run.variables["X"], 123.0)
        run.evalmodule.input(GrinTokenKind.INNUM, dummy_token, "123")
        self.assertEqual(run.variables["X"], 123)
        with self.assertRaises(Exception):
            run.evalmodule.input(GrinTokenKind.INNUM, dummy_token, "A.O")


class DummyToken:
    """Used to test input."""
    def __init__(self, value):
        self._value = value

    def value(self):
        """Returns value."""
        return self._value

dummy_token = DummyToken("X")