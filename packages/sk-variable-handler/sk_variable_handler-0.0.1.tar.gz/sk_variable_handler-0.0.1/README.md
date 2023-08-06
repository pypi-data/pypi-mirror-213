# Variable Handler

This is a Python package that provides a `VariableHandler` class for extracting variable values from a string of variable declarations.

## Installation

To use the `VariableHandler` package, you need to install it first. You can install it using pip:

```shell
pip install sk_variable_handler
```

## Usage

To extract variable values from a string of variable declarations, follow these steps:

1. Import the `VariableHandler` class from the `variable_handler` module:

   ```python
   from sk_variable_handler import VariableHandler
   ```

2. Create an instance of the `VariableHandler` class:

   ```python
   variable_handler = VariableHandler()
   ```

3. Call the `get_values` method of the `VariableHandler` instance, passing the string of variable declarations as an argument. It returns a dictionary containing the variable names as keys and their corresponding values as values.

   ```python
   declarations = "Your variable declarations"
   values = variable_handler.get_values(declarations)
   ```

### Example

Here is an example that demonstrates the usage of the `VariableHandler`:

```python
from variable_handler import VariableHandler

variable_handler = VariableHandler()

declarations = "$x=1+2;$y=2+1;$var=12+223+(222+2)+sin(90);$var2=$x+$y;$xy=($var2+$x+$y);$yx=$xy+$var2"
expected_result = {'$x': '3.0', '$y': '3.0', '$var': '460.0', '$var2': '6.0', '$xy': '12.0', '$yx': '18.0'}

result = variable_handler.get_values(declarations)
assert result == expected_result
```

## Test Cases

The package includes a set of unit tests to verify the functionality of the `VariableHandler` class. The tests cover various scenarios and edge cases to ensure the correct extraction of variable values.

To run the tests, execute the script as a standalone Python program:

```shell
python <filename>.py
```

The output will indicate whether all the tests have passed or if there are any failures.

Please note that the tests are implemented using the `unittest` framework. Each test case is independent and tests a specific aspect of the `VariableHandler` functionality.

## Contributing

Contributions to the `VariableHandler` package are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please create a pull request or open an issue on the GitHub repository.

## License

The `VariableHandler` package is distributed under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](LICENSE) file for more information.