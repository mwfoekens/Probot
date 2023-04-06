from robot.api import TestSuite


def generate_testsuite(data):
    print(data)
    print(type(data))
    get_testsuites(data)


def get_testsuites(received_data):
    data = TestSuite.from_file_system("")
    test_suite = []
    for suite in data.suites:
        test_suite.extend([a for a in suite.tests for b in received_data if a.name == b])

    if len(received_data) != len(test_suite):
        raise IndexError("Not all test cases were found")


a = ["Test Case NoTag/D 1.2", "Test Case NoTag/D 2.1"]
get_testsuites(a)
