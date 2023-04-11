from robot.api import TestSuite, ResultWriter


def prepare(data):
    """
    Method that prepares the data and generates test suites
    :param data: data that was received by receiver
    :return:
    """
    test_cases, imports = get_testcase_objects(data)
    suite = generate_testsuite_from_data(test_cases, imports)
    print(suite.tests)
    suite.run(output="./outputlog/output.xml", outputdir="outputlog")
    ResultWriter("./outputlog/output.xml").write_results()


def get_testcase_objects(received_data):
    """
    Get the test case objects that correspond to the test suite names
    :param received_data: test case names
    :return: the test case order and the imports
    """
    data = TestSuite.from_file_system("")
    test_case_objects = []
    imports = set()
    for suite in data.suites:
        imports.update(get_imports(suite))
        test_case_objects.extend([a for a in suite.tests for b in received_data if a.name == b])

    if len(received_data) != len(test_case_objects):
        raise IndexError("Not all test cases were found")

    return maintain_test_case_order(received_data, test_case_objects), imports


def get_imports(suite):
    """
    get imports from a test suite
    :param suite: a test suite
    :return: all test suite imports
    """
    imports = set()
    for imported_item in suite.resource.imports:
        imports.add(imported_item)
    return imports


def maintain_test_case_order(received_data, test_case_objects):
    """
    Sort the test case objects so that the order of the :var received_data and the :var test_case_objects are the same
    :param received_data: the cluster
    :param test_case_objects: the test case objects
    :return: :var test_case_objects, but the same order as :var received_data
    """
    sorted_list = []
    for i in range(len(received_data)):
        for y in range(len(test_case_objects)):
            if received_data[i] == test_case_objects[y].name:
                sorted_list.insert(i, test_case_objects[y])

    return sorted_list


def generate_testsuite_from_data(test_cases, imports, test_suite_name="Temporary TestSuite"):
    """
    Generate a test suite with all the test cases, and import all necessary imports
    :param test_cases: the test cases
    :param imports: the imports this suite will require
    :param test_suite_name: Name of the testsuite
    :return: the test suite
    """
    suite = TestSuite(test_suite_name)
    for import_item in imports:
        suite.resource.imports.library(import_item.name)

    for test in test_cases:
        t = suite.tests.create(name=test.name)

        for keyword in test.body:
            t.body.create_keyword(keyword.name, args=keyword.args)

    return suite


a = ["Test Case NoTag/D 1.2", "Test Case NoTag/D 2.1", "Test Case D 1.1.1"]
prepare(a)
