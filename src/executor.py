import robot.errors
from robot.api import TestSuite
from pathlib import PurePath

COUNT = 0


def prepare(data: list, output_path_location: str, test_suite_name: str):
    """
    Method that prepares the data and generates test suites
    :param data: data that was received by receiver
    :param output_path_location:
    :param test_suite_name:
    :return:
    """
    test_cases, imports = get_testcase_objects(data)
    suite = generate_testsuite_from_data(test_cases, imports, test_suite_name)
    execute(suite, PurePath(output_path_location), test_suite_name)


def execute(suite: TestSuite, output_path_location: PurePath, test_suite_name: str):
    """
    Execute the test suite and store information at a custom location
    :param suite: the test suite
    :param output_path_location: the output location
    :param test_suite_name:
    :return:
    """
    suite.run(outputdir=output_path_location, output=f"{test_suite_name}-{str(COUNT)}-output.xml")


def get_testcase_objects(received_data: list):
    """
    Get the test case objects that correspond to the test suite names
    :param received_data: test case names
    :return: the test case order and the imports
    """
    try:
        # docker
        data = TestSuite.from_file_system(PurePath("test-suites"))
    except robot.errors.DataError:
        # local test
        data = TestSuite.from_file_system(PurePath("../suites"))

    test_case_objects = []
    imports = set()

    for suite in data.suites:
        imports.update(get_imports(suite))
        test_case_objects.extend([test_case_object for test_case_object in suite.tests for test_name in received_data if
                                  test_case_object.name == test_name])

    if len(received_data) != len(test_case_objects):
        raise IndexError("Not all test cases were found")

    return maintain_test_case_order(received_data, test_case_objects), imports


def get_imports(suite: TestSuite):
    """
    get imports from a test suite
    :param suite: a test suite
    :return: all test suite imports
    """
    imports = set()
    for imported_item in suite.resource.imports:
        imports.add(imported_item)
    return imports


def maintain_test_case_order(received_data: list, test_case_objects: list):
    """
    Sort the test case objects so that the order of the :var received_data and the :var test_case_objects are the same
    :param received_data: the cluster
    :param test_case_objects: the test case objects
    :return: :var test_case_objects, but the same order as :var received_data
    """
    sorted_list = []
    for index_received_data in range(len(received_data)):
        for index_test_case_objects in range(len(test_case_objects)):

            if received_data[index_received_data] == test_case_objects[index_test_case_objects].name:
                sorted_list.insert(index_received_data, test_case_objects[index_test_case_objects])
                break

    return sorted_list


def generate_testsuite_from_data(test_cases: list, imports: set, test_suite_name: str):
    """
    Generate a test suite with all the test cases, and import all necessary imports
    :param test_cases: a list of test cases
    :param imports: the imports this suite will require
    :param test_suite_name: Name of the testsuite
    :return: the test suite
    """
    suite = TestSuite(str(test_suite_name) + " Suite: " + str(COUNT))
    for import_item in imports:
        suite.resource.imports.library(import_item.name)

    for test in test_cases:
        test_case = suite.tests.create(name=test.name)
        test_case.tags = test.tags

        for keyword in test.body:
            test_case.body.create_keyword(keyword.name, args=keyword.args)

    return suite

# a = ["Test Case NoTag/D 1.2", "Test Case NoTag/D 2.1", "Test Case D 1.1.1"]
# prepare(a)
