import collections
import unittest
from pathlib import PurePath

from robot.api import TestSuite
from robot.running.model import TestCase

import src.executor as e

test_cases = ['Test Case D 1.1.1', 'Test Case NoTag/D 2.1', 'Test Case NoTag/D 1.2']
test_case_objects, imports, keywords = e.get_testcase_objects(test_cases)


class ConsumerTests(unittest.TestCase):
    def test_generate_test_suite_from_data(self):
        suite = e.generate_testsuite_from_data(test_case_objects, imports, keywords, f"TEST " + str(e.COUNT))
        self.assertEqual(type(suite.tests[1]), TestCase)

    def test_maintain_order(self):
        data = TestSuite.from_file_system(PurePath("unittest-suites"))
        _test_case_objects = []

        for suite in data.suites:
            _test_case_objects.extend(
                [test_case_object for test_case_object in suite.tests for test_name in test_cases if
                 test_case_object.name == test_name])

        sorted_list = e.maintain_test_case_order(test_cases, _test_case_objects)
        self.assertEqual(sorted_list[2].name, test_cases[2])

    def test_if_new_suite_imports_user_keywords(self):
        suite = TestSuite(name="Test Test Suite")
        e.add_keywords_to_suite(suite, keywords)

        keyword_names = []
        for keyword in suite.resource.keywords:
            keyword_names.append(keyword.name)

        self.assertTrue(collections.Counter(keyword_names) == collections.Counter(
            ["Simple Keyword", "Add New Todo \"${todo}\"", "Open ToDo App"]))

    def test_if_new_suite_imports_imports(self):
        suite = TestSuite(name="Test Test Suite")
        e.add_imports_to_suite(suite, imports)
        import_names = []
        for import_item in suite.resource.imports:
            import_names.append(import_item.name)

        lib1 = "my_robot_func.py"
        lib2 = "Browser"
        filtered = set(i for i in import_names if lib1 in str(i) or lib2 in str(i))
        self.assertTrue(len(filtered) == 3)

    def test_if_new_suite_adds_tests(self):
        suite = TestSuite(name="Test Test Suite")
        e.add_tests_to_suite(suite, test_case_objects)

        for i in range(len(suite.tests)):
            self.assertEqual(len(suite.tests[i].body), len(test_case_objects[i].body))


if __name__ == '__main__':
    unittest.main()
