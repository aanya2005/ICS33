import unittest
from grin.processing import Running
from grin import GrinTokenKind, GrinToken, processing
from grin.exception_handling import GrinException
from project3 import main

class TestGrinFunctionality(unittest.TestCase):
    def test_let(self):
        run = Running()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 0)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = 'B', location = None,
                           value = 3)
        run.let(token1, token2)
        self.assertEqual(run.variables['A'], 3)
        token3 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'C', location = None,
                           value = 5)
        run.variables['C'] = 5
        run.let(token1, token3)
        self.assertEqual(run.variables['A'], 5)
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 0)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = 'B', location = None,
                           value = 3)
        run.op(GrinTokenKind.LET, token1, token2)
        self.assertEqual(run.variables['A'], 3)


    def test_preprocess_function(self):
        program = Running()
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        self.assertEqual(program.program,[])
        program.preprocess()
        self.assertNotEqual(program.program, None)
        self.assertEqual(len(program.program),2)

    def test_runnable_function(self):
        program = Running()
        self.assertFalse(program.runnable())
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        program.preprocess()
        self.assertTrue(program.runnable())

    def test_forward_function(self):
        program = Running()
        program.forward()
        self.assertEqual(program.counter, 1)

    def test_end_function(self):
        program = Running()
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        program.preprocess()
        program.end()
        self.assertEqual(program.counter, len(program.program))
        self.assertFalse(program.runnable())

    def test_eval_function(self):
        program = Running()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '9', location = None,
                           value = 9)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 2.0)
        token3 = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = 'Job', location = None,
                           value = 'Job')

        program.variables['9'] = 9
        program.variables['Job'] = 'Job'

        self.assertTrue(program.eval(token1, GrinTokenKind.GREATER_THAN, token2, None))
        self.assertTrue(program.eval(token1, GrinTokenKind.GREATER_THAN_OR_EQUAL, token2, None))
        self.assertFalse(program.eval(token1, GrinTokenKind.LESS_THAN, token2, None))
        self.assertFalse(program.eval(token1, GrinTokenKind.LESS_THAN_OR_EQUAL, token2, None))
        self.assertTrue(program.eval(token1, GrinTokenKind.NOT_EQUAL, token2, None))
        self.assertFalse(program.eval(token1, GrinTokenKind.EQUAL, token2, None))
        self.assertRaises(GrinException, program.eval, token1, GrinTokenKind.NOT_EQUAL,
                          token3, None)

    def test_goto_function(self):
        program = Running()
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        program.add_command('GOTO 2')
        program.add_command('PRINT A')
        program.add_command('PRINT B')
        program.add_command('PRINT A')
        program.add_command('PRINT B')
        program.add_command('PRINT A')
        program.add_command('PRINT B')
        token1 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 2)
        token2 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 3)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        program.jump(GrinTokenKind.GOTO, token1, None)
        self.assertEqual(program.counter, 4)
        program.jump(GrinTokenKind.GOTO, token2, None)
        self.assertEqual(program.counter, 3)

    def test_gosub_function(self):
        program = Running()
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        program.add_command('GOSUB 2')
        program.add_command('PRINT A')
        program.add_command('PRINT B')
        program.add_command('PRINT A')
        program.add_command('PRINT B')
        program.add_command('PRINT A')
        program.add_command('PRINT B')
        token1 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 2)
        token2 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 3)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        program.jump(GrinTokenKind.GOSUB, token1, None)
        self.assertEqual(program.counter, 4)
        program.jump(GrinTokenKind.GOSUB, token2, None)
        self.assertEqual(program.counter, 3)

    def test_goto_zero(self):
        program = Running()
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        program.add_command('GOTO 0')
        token1 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 0)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        with self.assertRaises(GrinException):
            program.jump(GrinTokenKind.GOTO, token1, None)

    def test_gosub_zero(self):
        program = Running()
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        program.add_command('GOSUB 0')
        program.add_command('.')
        token1 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 0)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        with self.assertRaises(GrinException):
            program.jump(GrinTokenKind.GOSUB, token1, None)

    def test_gosub_none(self):
        program = Running()
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        program.add_command('GOSUB 0')
        program.add_command('.')
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = None, location = None,
                           value = None)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        with self.assertRaises(GrinException):
            program.jump(GrinTokenKind.GOSUB, token1, None)

    def test_goto_none(self):
        program = Running()
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        program.add_command('GOTO 0')
        program.add_command('.')
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = None, location = None,
                           value = None)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        with self.assertRaises(GrinException):
            program.jump(GrinTokenKind.GOTO, token1, None)

    def test_return_function(self):
        program = Running()
        program.add_command('LET A 1')
        program.add_command('LET B 2')
        program.add_command('GOTO 2')
        program.add_command('PRINT A')
        program.add_command('PRINT B')
        program.add_command('PRINT A')
        program.add_command('PRINT B')
        program.add_command('PRINT A')
        program.add_command('PRINT B')
        token1 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 2)
        token2 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 3)
        program.preprocess()
        program.functions['A'] = 3
        program.counter = 2
        program.jump(GrinTokenKind.GOSUB, token1, None)
        program.backtrack()
        self.assertEqual(program.counter, 3)
        program.jump(GrinTokenKind.GOSUB, token2, None)
        program.backtrack()
        self.assertEqual(program.counter, 4)

    def test_get_statement(self):
        run = Running()
        run.program = "PRINT A"
        self.assertEqual(run.get_statement(),"P")
    def test_backtrack(self):
        program = Running()
        program.stack = []
        program.backtrack()
        self.assertEqual(program.counter, 1)
