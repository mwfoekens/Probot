import robot.result
from robot.api import TestSuite, ExecutionResult
from robot.model.testsuite import TestSuites
from pathlib import Path
from random import choice
import json
import click


def main(dependency_file: str, output: str, time_group_size: int, random_group_size: int, suites_location) -> list:
    """
    Splits test suite into multiple groups

    :param dependency_file:     The file containing dependencies
    :param output:              xml file containing runtimes of the previous run
    :param time_group_size:   Amount of groups for groups split on time
    :param random_group_size: Amount of groups for groups that are randomly assigned
    :param suites_location:     Location of the suites
    :return:                    Groups
    """
    groups: list = []
    modulo_group: list = []
    result: ExecutionResult = (TestSuite.from_file_system(Path(suites_location))
                               .run(dryrun=True, outputdir=Path("../dryrunlog")))

    # If there is a dependency.json, read it and generate groups for it
    if dependency_file:
        with open(dependency_file, "r") as json_file:
            file: dict = json.load(json_file)
        dependency_group: list = generate_groups(file["dependencies"])
        tags_group: list = generate_groups(file["tags"])
    else:
        dependency_group: list = []
        tags_group: list = []
        click.secho("No dependency.json passed.", fg='bright_red', bg='white')

    # Always append a test to the leftover group, it gets removed when it fits into a dependency group
    for suite in result.suite.suites:
        for test in suite.tests:
            modulo_group.append(test.name)

            if dependency_file:
                dependency_sort(dependency_group, file, modulo_group, tags_group, test)

    # Add the dependency group and tag group to all groups
    if dependency_file:
        groups.extend(dependency_group)
        groups.extend(tags_group)

    # if there is an output.xml, retrieve the times and sort based on execution time.
    if output:
        outputxml_group = outputxml_sort(modulo_group, output, time_group_size)
        groups.extend(outputxml_group)
    else:
        click.secho("No output.xml passed", fg='bright_red', bg='white')

    # If we have tests left, assign randomly, because there's no data about the tests.
    if len(modulo_group) != 0:
        random_groups: list = generate_groups(random_group_size)

        for test in modulo_group:
            choice(random_groups).append(test)
        groups.extend(random_groups)

    return [group for group in groups if len(group) != 0]


def outputxml_sort(modulo_group: list, output: str, time_group_size: int) -> list:
    """
    Sort based on execution times
    :param modulo_group:      Group where the leftover test cases are stored
    :param output:              Output.xml file
    :param time_group_size:   Size for the timed Groups
    :return:                    Groups
    """
    execution_times: dict = dict()
    timed_groups: list = generate_groups(time_group_size)
    time_groups_names: list = generate_groups(time_group_size)

    data: ExecutionResult = ExecutionResult(Path(output), merge=False)

    loop_location = find_test_suites(data)

    # Gather tests
    for suite in loop_location:
        for test in suite.tests:

            if test.name in modulo_group:
                add_to_group_and_remove_from_modulo_group(execution_times, None, modulo_group, test)

    greedy_sort(execution_times, time_groups_names, timed_groups)

    return time_groups_names


def find_test_suites(data: ExecutionResult) -> TestSuites:
    """
    For some reason Robot tests can be nested quite far in :var data, so this method should help find
    where the actual test suites are so it can be looped over
    :param data: A robot execution result object
    :return: the location where the actual suites are.
    """
    loop_location = data.suite.suites
    while len(loop_location) == 1 and len(loop_location[0].tests) == 0:
        loop_location = loop_location[0].suites
        
    return loop_location


def greedy_sort(execution_times: dict, time_groups_names: list, timed_groups: list) -> None:
    """
    Assigns tests to groups in descending order.
    :param execution_times:         Dictionary where test names and their execution times are stored
    :param time_groups_names:     Names of the tests only
    :param timed_groups:          Times of the tests only
    :return:                        None
    """
    for test, time in dict(sorted(execution_times.items(), key=lambda x: x[1], reverse=True)).items():
        sum_per_group: list = [sum(timed_groups) for timed_groups in timed_groups]
        index: int = sum_per_group.index(min(sum_per_group))
        timed_groups[index].append(time)
        time_groups_names[index].append(test)


def dependency_sort(dependency_group: list, file: dict, modulo_group: list, tags_group: list, test) -> None:
    """
    Sort into groups based on dependencies
    :param dependency_group:  Group containing test cases with direct dependencies
    :param file:                File where dependencies are stored
    :param modulo_group:      Group where leftover test cases are stored
    :param tags_group:        Group where test cases with a tag mentioned in the dependency file are stored
    :param test:                The individual test to be sorted
    :return:                    None
    """
    found_in_dependency: bool = False
    found_in_tags: bool = False

    for dependency_index in range(len(file["dependencies"])):

        if test.name in file["dependencies"][dependency_index]:
            add_to_group_and_remove_from_modulo_group(dependency_group, dependency_index, modulo_group, test)
            found_in_dependency = True

    for tags_index in range(len(file["tags"])):

        if file["tags"][tags_index] in test.tags and found_in_dependency is False and found_in_tags is False:
            add_to_group_and_remove_from_modulo_group(tags_group, tags_index, modulo_group, test)
            found_in_tags = True


def add_to_group_and_remove_from_modulo_group(group: list or dict, test_index: int or None,
                                              modulo_group: list, test: robot.result.TestCase) -> None:
    """
    Add test to a new group group, and remove from the modulo group
    :param group:   group to be added to
    :param test_index:      Index of the group to be added to
    :param modulo_group:  Leftover test case group.
    :param test:            Test in question.
    :return:                None
    """
    if type(group) is dict:
        group[test.name] = (test.elapsedtime / 1000)
    else:
        group[test_index].append(test.name)
    modulo_group.remove(test.name)


def generate_groups(group_size: int or list) -> list:
    """
    Generate groups within a group
    :param group_size:    The size of the group
    :return:                A group with :var: group_size amount of groups
    """
    if type(group_size) is int:
        return [[] for _ in range(group_size)]
    else:
        return [[] for _ in group_size]
