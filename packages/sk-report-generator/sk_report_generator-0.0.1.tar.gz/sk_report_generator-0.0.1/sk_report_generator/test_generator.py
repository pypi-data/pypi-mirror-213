from sk_report_generator.report_generator import ReportGenerator

import unittest

class ReportGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.report_generator = ReportGenerator()

    def test_generate_report(self):

        template = 'Rohim has {{$x:.2f}} taka and Korim has $y taka. They have $xy taka. The can get $var taka. They need $var2 taka and $yx'
        data = {'$x': '3.00000099999999', '$y': '3.0', '$var': '460.0', '$var2': '6.00000099999999', '$xy': '12.00000199999998', '$yx': '18.00000299999997'}
        expected_output = 'Rohim has 3.00 taka and Korim has 3.0 taka. They have 12.00000199999998 taka. The can get 460.0 taka. They need 6.00000099999999 taka and 18.00000299999997'

        output = self.report_generator.generate_report(template, data)

        self.assertEqual(output, expected_output)

    def test_generate_report2(self):
        # Test case 1: Basic substitution
        template = 'Hello, {{$name}}!'
        data = {'$name': 'John'}
        expected_output = 'Hello, John!'
        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)

        # Test case 2: Formatting and multiple substitutions
        template = 'Total amount: $total_amount. Discount: {{$discount:.2f}}%. Final amount: $final_amount.'
        data = {'$total_amount': '1000', '$discount': '15.5', '$final_amount': '845.00'}
        expected_output = 'Total amount: 1000. Discount: 15.50%. Final amount: 845.00.'
        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)

        # Test case 3: Substitution not present in data
        template = 'Hello, {{$name}}!'
        data = {'$age': '25'}
        expected_output = 'Hello, {{$name}}!'
        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)

        # Test case 4: Empty template and data
        template = ''
        data = {}
        expected_output = ''
        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)

    def test_generate_report3(self):
        # Test case 1: Substitution with integer value
        template = 'The answer is {{$number}}.'
        data = {'$number': 42}
        expected_output = 'The answer is 42.'
        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)

        # Test case 2: Substitution with string value
        template = 'The color is {{$color}}.'
        data = {'$color': 'blue'}
        expected_output = 'The color is blue.'
        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)

        # Test case 3: Substitution with float value and custom format
        template = 'The price is ${{ $price:.2f }}.'
        data = {'$price': 19.99}
        expected_output = 'The price is $19.99.'

        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)

        # Test case 4: Substitution with missing key in data
        template = 'The name is {{$name}}.'
        data = {}
        expected_output = 'The name is {{$name}}.'

        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)

        # Test case 5: Template with multiple occurrences of the same variable
        template = 'The number is {{$number}} and {{$number}}.'
        data = {'$number': 7}
        expected_output = 'The number is 7 and 7.'

        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)
    def test_extra(self):
        template = 'The number is {{$number}} and {{$number}} binary = {{$number:b}}.'
        data = {'$number': 7}
        expected_output = 'The number is 7 and 7 binary = 111.'

        output = self.report_generator.generate_report(template, data)
        self.assertEqual(output, expected_output)
if __name__ == '__main__':
    unittest.main()
