import unittest
from grin.processing import Running
from grin import GrinTokenKind, GrinToken
from grin.exception_handling import GrinException


class TestGrinFunctionality(unittest.TestCase):

    def test_add_functionality(self):
        run = Running()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None, value = 5)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 3)
        run.variables['A'] = 5
        run.op(GrinTokenKind.ADD, token1, token2)
        self.assertEqual(run.variables['A'], 8)

        token3 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'B', location = None, value = 2.6)
        token4 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None, value = 3.4)
        run.variables['B'] = 2.6
        run.op(GrinTokenKind.ADD, token3, token4)
        self.assertEqual(run.variables['B'], 6.0)

        token5 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'C', location = None,
                           value = 3)
        token6 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 3.4)
        run.variables['C'] = 3
        run.op(GrinTokenKind.ADD, token5, token6)
        self.assertEqual(run.variables['C'], 6.4)

        token7 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'HELLO', location = None,
                           value = 'HELLO')
        token8 = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = 'BOO', location = None,
                           value = 'BOO')
        run.variables['HELLO'] = 'HELLO'
        run.op(GrinTokenKind.ADD, token7, token8)
        self.assertEqual(run.variables['HELLO'], 'HELLOBOO')

        token9 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'TEST', location = None,
                           value = 'TEST')
        token10 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                            value = 3.2)
        run.variables['TEST'] = 'TSET'
        self.assertRaises(GrinException, run.op, GrinTokenKind.ADD, token9, token10)
        token11 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'HELLO', location = None,
                           value = 'HELLO')
        token12 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = 'BOO', location = None,
                           value = 2.5)
        self.assertRaises(GrinException, run.op, GrinTokenKind.ADD, token11, token12)
        token13 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'B', location = None,
                           value = 2.6)
        token14 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 3.4)
        run.variables['B'] = 2.6
        run.op(GrinTokenKind.ADD, token13, token14)
        token15 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '', location = None,
                           value = 3.6)
        token16 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = 'TEST', location = None,
                            value = 'TEST')
        run.variables['TEST'] = 'TSET'
        self.assertRaises(GrinException, run.op, GrinTokenKind.ADD, token15, token16)

    def test_subtraction_functionality(self):
        program = Running()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'D', location = None, value = 3.2)
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 1.1)
        program.variables['D'] = 3.2
        program.op(GrinTokenKind.SUB, token1, token2)
        self.assertEqual(program.variables['D'], 2.1)

        token3 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'E', location = None,
                           value = 3)
        token4 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 1.1)
        program.variables['E'] = 3
        program.op(GrinTokenKind.SUB, token3, token4)
        self.assertEqual(program.variables['E'], 1.9)

        token5 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'EXAMPLE', location = None,
                           value = 'EXAMPLE')
        token6 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                            value = 3.2)
        program.variables['EXAMPLE'] = 'EXAMPLE'
        self.assertRaises(GrinException, program.op, GrinTokenKind.SUB, token5, token6)
        token7 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'E', location = None,
                           value = 3)
        token8 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'F', location = None,
                           value = 1.1)
        program.variables['E'] = 3
        program.variables['F'] = 1.1
        program.op(GrinTokenKind.SUB, token7, token8)
        self.assertEqual(program.variables['E'], 1.9)

    def test_multiplication_functionality(self):
        program = Running()
        token5 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'Hi', location = None,
                           value = 'Hi')
        token6 = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = 'World', location = None,
                           value = 'World')
        program.variables['Hi'] = 'Hi'
        self.assertRaises(GrinException, program.op, GrinTokenKind.MULT, token5, token6)
        token7 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'Boo', location = None,
                           value = 'Boo')
        token8 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 3)
        program.variables['Boo'] = 'Boo'
        program.op(GrinTokenKind.MULT, token8, token7)
        self.assertEqual(program.variables['Boo'], 'Boo')

    def test_division_functionality(self):
        program = Running()
        token1 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '7', location = None,
                           value = 7 )
        token2 = GrinToken(kind = GrinTokenKind.LITERAL_INTEGER, text = '', location = None,
                           value = 2)
        program.variables['7'] = 7
        program.op(GrinTokenKind.DIV, token1, token2)
        self.assertEqual(program.variables['7'], 3)

        token3 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '9', location = None,
                           value = 9)
        token4 = GrinToken(kind = GrinTokenKind.LITERAL_FLOAT, text = '', location = None,
                           value = 2.0)
        program.variables['9'] = 9
        program.op(GrinTokenKind.DIV, token3, token4)
        self.assertEqual(program.variables['9'], 4.5)

        token5 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'Good', location = None,
                           value = 'Good')
        token6 = GrinToken(kind = GrinTokenKind.LITERAL_STRING, text = 'Job', location = None,
                           value = 'Job')
        program.variables['Good'] = 'Good'
        self.assertRaises(GrinException, program.op, GrinTokenKind.DIV, token5, token6)
        token7 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 9)
        token8 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'B', location = None,
                           value = 2.0)
        program.variables['A'] = 9
        program.variables['B'] = 2.0
        program.op(GrinTokenKind.DIV, token7, token8)
        self.assertEqual(program.variables['9'], 4.5)
        token9 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '9', location = None,
                           value = 9)
        token10 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = '10', location = None,
                           value = 2.0)
        program.variables['A'] = 'A'
        self.assertRaises(GrinException, program.op, GrinTokenKind.DIV, token9, token10)
        token11 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'A', location = None,
                           value = 9)
        token12 = GrinToken(kind = GrinTokenKind.IDENTIFIER, text = 'B', location = None,
                           value = 2)
        program.variables['A'] = 9
        program.variables['B'] = 2
        program.op(GrinTokenKind.DIV, token11, token12)
        self.assertEqual(program.variables['9'], 4.5)
