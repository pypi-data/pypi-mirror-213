# Report Generator

This is a Python package that provides a `ReportGenerator` class for generating reports by replacing placeholders in a template with corresponding values from a data dictionary.

## Installation

To use the `ReportGenerator` package, you need to install it first. You can install it using pip:

```shell
pip install sk_report_generator
```

## Usage

To generate a report, follow these steps:

1. Import the `ReportGenerator` class from the `sk_report_generator.report_generator` module:

   ```python
   from sk_report_generator.report_generator import ReportGenerator
   ```

2. Create an instance of the `ReportGenerator` class:

   ```python
   report_generator = ReportGenerator()
   ```

3. Define your template string, containing placeholders for substitution. Placeholders are specified using the format `{{$placeholder}}`.

4. Prepare a data dictionary that maps placeholder names to their corresponding values.

5. Call the `generate_report` method of the `ReportGenerator` instance, passing the template and data as arguments. It returns the generated report string.

   ```python
   template = 'Your template string'
   data = {'$placeholder1': 'value1', '$placeholder2': 'value2'}
   report = report_generator.generate_report(template, data)
   ```

### Example

Here is an example that demonstrates the usage of the `ReportGenerator`:

```python
from sk_report_generator.report_generator import ReportGenerator

report_generator = ReportGenerator()

template = 'Hello, {{$name}}!'
data = {'$name': 'John'}
expected_output = 'Hello, John!'

output = report_generator.generate_report(template, data)
assert output == expected_output
```

## Test Cases

The package includes a set of unit tests to verify the functionality of the `ReportGenerator` class. The tests cover various scenarios and edge cases to ensure the correct behavior of the package.

To run the tests, execute the script as a standalone Python program:

```shell
python <filename>.py
```

The output will indicate whether all the tests have passed or if there are any failures.

Please note that the tests are implemented using the `unittest` framework. Each test case is independent and tests a specific aspect of the `ReportGenerator` functionality.

## Contributing

Contributions to the `ReportGenerator` package are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please create a pull request or open an issue on the GitHub repository.

## License

The `ReportGenerator` package is distributed under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](LICENSE) file for more information.