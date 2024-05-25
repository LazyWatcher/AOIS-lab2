import unittest

from main import print_truth_table, get_index_form, get_numerical_form, build_pcnf, build_pdnf


class MyTestCase(unittest.TestCase):
    def test_something(self):
        expression = "((!a) & b) | c "
        truth_table_results, variables = print_truth_table(expression)
        binary_form = get_index_form(truth_table_results)
        test = '01110101'
        self.assertEqual(binary_form, test)  # add assertion here
    def test_something2(self):
        expression = "((!a) - b) ~ c "
        truth_table_results, variables = print_truth_table(expression)
        binary_form = get_index_form(truth_table_results)
        decimal_form = get_numerical_form(truth_table_results)
        test = 149
        pdnf = build_pdnf(truth_table_results, variables)
        print("SDNF:", pdnf)
        self.assertEqual(decimal_form, test)  # add assertion here
    def test_something3(self):
        expression = "((!a) - b) ~ (c & d) | e "
        truth_table_results, variables = print_truth_table(expression)
        binary_form = get_index_form(truth_table_results)
        decimal_form = get_numerical_form(truth_table_results)
        test = 4250359639
        pdnf = build_pdnf(truth_table_results, variables)
        print("SDNF:", pdnf)
        pcnf = build_pcnf(truth_table_results, variables)
        print("SKNF:", pcnf)
        self.assertEqual(decimal_form, test)  # add assertion here

if __name__ == '__main__':
    unittest.main()
