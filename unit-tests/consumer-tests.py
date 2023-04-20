import unittest

from robot.running.model import TestCase
from robot.api import TestSuite
from pathlib import PurePath

import src.executor as executor

test_cases = ['Test Case D 1.1.1', 'Test Case NoTag/D 2.1', 'Test Case NoTag/D 1.2']
test_case_objects, imports = executor.get_testcase_objects(test_cases)


class ConsumerTests(unittest.TestCase):
    def test_generate_test_suite_from_data(self):
        suite = executor.generate_testsuite_from_data(test_case_objects, imports, f"TEST " + str(executor.COUNT))
        self.assertEqual(type(suite.tests[1]), TestCase)

    def test_maintain_order(self):
        data = TestSuite.from_file_system(PurePath("unittest-suites"))
        _test_case_objects = []

        for suite in data.suites:
            _test_case_objects.extend(
                [test_case_object for test_case_object in suite.tests for test_name in test_cases if
                 test_case_object.name == test_name])

        sorted_list = executor.maintain_test_case_order(test_cases, _test_case_objects)
        self.assertEqual(sorted_list[2].name, test_cases[2])


if __name__ == '__main__':
    unittest.main()
