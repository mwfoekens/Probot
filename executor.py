from robot.api import TestSuite, ResultWriter


def prepare(data):
    test_cases = get_testcase_objects(data)
    generate_testsuite_from_data(test_cases)


def get_testcase_objects(received_data):
    data = TestSuite.from_file_system("")
    test_case_objects = []
    for suite in data.suites:
        test_case_objects.extend([a for a in suite.tests for b in received_data if a.name == b])

    if len(received_data) != len(test_case_objects):
        raise IndexError("Not all test cases were found")

    return maintain_test_case_order(received_data, test_case_objects)


def maintain_test_case_order(received_data, test_case_objects):
    sorted_list = []
    for i in range(len(received_data)):
        for y in range(len(test_case_objects)):
            if received_data[i] == test_case_objects[y].name:
                sorted_list.insert(i, test_case_objects[y])

    return sorted_list


def generate_testsuite_from_data(data):
    suite = TestSuite("TEST TestSuite")
    suite.resource.imports.library("Browser")
    for test in data:
        t = suite.tests.create(name=test.name)
        t.body.create_keyword("Log", args=["HIIIIIIIII"])
    suite.run(output="./outputlog/output.xml")
    ResultWriter("./outputlog/output.xml").write_results()


a = ["Test Case NoTag/D 1.2", "Test Case NoTag/D 2.1", "Test Case D 1.1.1"]
prepare(a)
