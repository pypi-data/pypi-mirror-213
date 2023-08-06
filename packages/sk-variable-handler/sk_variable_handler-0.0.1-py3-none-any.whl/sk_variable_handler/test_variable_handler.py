from variable_handler import VariableHandler
from sk_calculator import Calculator
import unittest
class TestGetValues(unittest.TestCase):
    def setUp(self):
        self.variable =VariableHandler()
        self.calculator = Calculator()
        self.variable.set_calculator(self.calculator)


    def test_get_values(self):
        declarations = "$x=1+2;$y=2+1;$var=12+223+(222+2)+sin(90);$var2=$x+$y;$xy=($var2+$x+$y);$yx=$xy+$var2"
        expected_result = {'$x': '3.0', '$y': '3.0', '$var': '460.0', '$var2': '6.0', '$xy': '12.0', '$yx': '18.0'}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)
    def test_get_values_empty_declaration(self):
        # Test when there are no variable declarations
        declarations = ""
        expected_result = {}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)

    def test_get_values_single_declaration(self):
        # Test when there is only one variable declaration
        declarations = "$x=10"
        expected_result = {'$x': '10.0'}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)

    def test_get_values_multiple_declarations(self):
        # Test when there are multiple variable declarations
        declarations = "$x=1;$y=2;$z=3"
        expected_result = {'$x': '1.0', '$y': '2.0', '$z': '3.0'}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)

    def test_get_values_duplicate_declarations(self):
        # Test when there are duplicate variable declarations
        declarations = "$x=1;$y=2;$x=3"
        expected_result = {'$x': '3.0', '$y': '2.0'}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)

    def test_get_values_invalid_declaration(self):
        # Test when there is an invalid variable declaration
        declarations = "$x=1+"
        expected_result = {'$x': "['Syntax Error: Incomplete expression at 1+']"}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)

    def test_get_values_with_spaces(self):

        # Test when there are spaces in the variable declarations
        declarations = "$x = 1 + 2 ; $y = 2 + 1 ; $var = 12 + 223 + (222 + 2) + sin(90) ; $var2 = $x + $y ; $xy = ($var2 + $x + $y) ; $yx = $xy + $var2"
        expected_result = {'$x': '3.0', '$y': '3.0', '$var': '460.0', '$var2': '6.0', '$xy': '12.0', '$yx': '18.0'}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)

    def test_get_values_case_sensitive(self):
        # Test when variable names are case sensitive
        declarations = "$X = 1 ; $x = 2 ; $X = $x + 3"
        expected_result = {'$X': '5.0', '$x': '2.0'}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)

    def test_get_values_with_trailing_semicolon(self):
        # Test when there is a trailing semicolon in the declarations
        declarations = "$x = 1 + 2 ;"
        expected_result = {'$x': '3.0'}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)

    def test_get_values_with_newlines(self):
        # Test when there are newlines in the variable declarations
        declarations = "$x = 1 + 2 ;\n$y = 2 + 1 ;\n$z = $x + $y"
        expected_result = {'$x': '3.0', '$y': '3.0', '$z': '6.0'}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)

    def test_get_values_with_comments(self):
        # Test when there are comments in the variable declarations
        declarations = "$x = 1 + 2 ; # Variable x\n$y = 2 + 1 ; # Variable y\n$z = $x + $y"
        expected_result = {'$x': '3.0', '$y': '3.0', '$z': '6.0'}
        result = self.variable.get_values(declarations)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()