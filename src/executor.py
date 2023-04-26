import os

from robot.api import TestSuite
from pathlib import PurePath

COUNT = 0


def prepare(data: list, output_path_location: str, test_suite_name: str) -> None:
    """
    Method that prepares the data and generates test suites
    :param data:                    data that was received by receiver
    :param output_path_location:    Location where data should be outputted
    :param test_suite_name:         Name of the test suite
    :return:                        None
    """
    test_cases, imports, keywords = get_testcase_objects(data)
    suite = generate_testsuite_from_data(test_cases, imports, keywords, test_suite_name)
    execute(suite, PurePath(output_path_location), test_suite_name)


def execute(suite: TestSuite, output_path_location: PurePath, test_suite_name: str) -> None:
    """
    Execute the test suite and store information at a custom location
    :param suite:                   the test suite
    :param output_path_location:    the output location
    :param test_suite_name:         Name of the test suite
    :return:                        None
    """
    suite.run(outputdir=output_path_location, output=f"{test_suite_name}-{str(COUNT)}-output.xml")


def get_testcase_objects(received_data: list) -> tuple:
    """
    Get the test case objects that correspond to the test suite names
    :param received_data:       test case names
    :return:                    the test case order and the imports
    """
    test_case_objects = []
    keywords = set()
    suite_location = find_test_suites()

    data = TestSuite.from_file_system(PurePath(suite_location))
    imports = set(extended_file for extended_file in os.scandir(PurePath(suite_location)) if
                  not extended_file.name.endswith(".robot") and extended_file.name != "__pycache__")

    for suite in data.suites:
        imports.update(get_imports(suite))
        keywords.update(get_keywords(suite))

        test_case_objects.extend([test_case_object for test_case_object in suite.tests for test_name in received_data if
                                  test_case_object.name == test_name])

    if len(received_data) != len(test_case_objects):
        raise IndexError("Not all test cases were found\n", received_data, test_case_objects)

    return maintain_test_case_order(received_data, test_case_objects), imports, keywords


def find_test_suites() -> str:
    """
    This function ensures the correct environment is always assumed. It should work still when ran locally.
    :return: location of the test suite
    """
    try:
        k8s = os.environ["EXECUTOR"]
    except KeyError:
        k8s = False

    if k8s:
        suite_location = "test-suites"
    else:
        suite_location = "../suites"
    return suite_location


def get_keywords(suite: TestSuite) -> set:
    """
    Get user defined keywords
    :param suite:   Suite we want to find the keywords from
    :return:        Set of keywords
    """
    return set(keyword for keyword in suite.resource.keywords)


def get_imports(suite: TestSuite) -> set:
    """
    get imports from a test suite
    :param suite:       a test suite
    :return:            all test suite imports
    """
    return set(imported_item for imported_item in suite.resource.imports)


def maintain_test_case_order(received_data: list, test_case_objects: list) -> list:
    """
    Sort the test case objects so that the order of the :var received_data and the :var test_case_objects are the same
    :param received_data:       the cluster
    :param test_case_objects:   the test case objects
    :return:                    :var test_case_objects, but the same order as :var received_data
    """
    sorted_list = []
    for index_received_data in range(len(received_data)):
        for index_test_case_objects in range(len(test_case_objects)):

            if received_data[index_received_data] == test_case_objects[index_test_case_objects].name:
                sorted_list.insert(index_received_data, test_case_objects[index_test_case_objects])
                break

    return sorted_list


def generate_testsuite_from_data(test_cases: list, imports: set, keywords: set, test_suite_name: str) -> TestSuite:
    """
    Generate a test suite with all the test cases, and import all necessary imports
    :param test_cases:      a list of test cases
    :param imports:         the imports this suite will require
    :param keywords:        User defined keywords for the suite
    :param test_suite_name: Name of the testsuite
    :return:                the test suite
    """
    suite = TestSuite(str(test_suite_name) + " Suite: " + str(COUNT))

    for import_item in imports:
        try:
            suite.resource.imports.library(PurePath(import_item.path))
        except AttributeError:
            suite.resource.imports.library(import_item.name)

    for keyword in keywords:
        suite.resource.keywords.append(keyword)

    for test in test_cases:
        test_case = suite.tests.create(name=test.name)
        test_case.tags = test.tags

        for keyword in test.body:
            test_case.body.create_keyword(keyword.name, args=keyword.args, assign=keyword.assign)

    return suite

# a = ["Test Case NoTag/D 1.2", "Test Case NoTag/D 2.1", "Test Case D 1.1.1", "Test Case Not In Output XML 2",
#      "Test Case Not In Output XML 1"]
# prepare(a, "log-combiner/test-output", "LOCAL TEST 1")
