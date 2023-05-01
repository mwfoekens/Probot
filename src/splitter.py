import robot.result
from robot.api import TestSuite, ExecutionResult
from pathlib import PurePath
from random import choice
import json
import click


def main(dependency_file: str, output: str, time_cluster_size: int, random_cluster_size: int, suites_location) -> list:
    """
    Splits test suite into multiple clusters

    :param dependency_file:     The file containing dependencies
    :param output:              xml file containing runtimes of the previous run
    :param time_cluster_size:   Amount of clusters for clusters split on time
    :param random_cluster_size: Amount of clusters for clusters that are randomly assigned
    :param suites_location:     Location of the suites
    :return:                    Clusters
    """
    clusters: list = []
    modulo_cluster: list = []
    result: ExecutionResult = retrieve_dry_run_results(suites_location)

    # If there is a dependency.json, read it and generate cluster groups for it
    if dependency_file is not None:
        with open(dependency_file, "r") as json_file:
            file: dict = json.load(json_file)
        dependency_cluster: list = generate_clusters(file["dependencies"])
        tags_cluster: list = generate_clusters(file["tags"])
    else:
        click.secho("No dependency.json passed.", fg='bright_red', bg='white')

    # Always append a test to the leftover cluster group, it gets removed when it fits into a dependency group
    for suite in result.suite.suites:
        for test in suite.tests:
            modulo_cluster.append(test.name)

            if dependency_file is not None:
                dependency_sort(dependency_cluster, file, modulo_cluster, tags_cluster, test)

    # Add the dependency cluster and tag cluster to all clusters
    if dependency_file is not None:
        add_cluster_group_to_all_clusters(clusters, dependency_cluster)
        add_cluster_group_to_all_clusters(clusters, tags_cluster)

    # if there is an output.xml, retrieve the times and sort based on execution time.
    if output is not None:
        add_cluster_group_to_all_clusters(clusters, outputxml_sort(modulo_cluster, output, time_cluster_size))
    else:
        click.secho("No output.xml passed", fg='bright_red', bg='white')

    # If we have tests left, assign randomly, because there's no data about the tests.
    if len(modulo_cluster) != 0:
        add_cluster_group_to_all_clusters(clusters, random_sort(modulo_cluster, random_cluster_size))

    return remove_empty_clusters(clusters)


def random_sort(modulo_cluster: list, random_cluster_size: int) -> list:
    """
    Function that randomly assigns test cases that are not in dependency, and do not exist in the output.xml
    :param modulo_cluster:          Cluster where the leftover test cases are stored
    :param random_cluster_size:     Amount of clusters for randomly assigned test cases.
    :return:                        Clusters
    """
    random_clusters: list = generate_clusters(random_cluster_size)

    for test in modulo_cluster:
        choice(random_clusters).append(test)
    return random_clusters


def outputxml_sort(modulo_cluster: list, output: str, time_cluster_size: int) -> list:
    """
    Sort based on execution times
    :param modulo_cluster:      Cluster where the leftover test cases are stored
    :param output:              Output.xml file
    :param time_cluster_size:   Size for the timed clusters
    :return:                    Clusters
    """
    execution_times: dict = dict()
    timed_clusters: list = generate_clusters(time_cluster_size)
    time_clusters_names: list = generate_clusters(time_cluster_size)

    data: ExecutionResult = extract_xml(output)

    gather_tests(data, execution_times, modulo_cluster)

    greedy_sort(execution_times, time_clusters_names, timed_clusters)

    return time_clusters_names


def gather_tests(data: ExecutionResult, execution_times: dict, modulo_cluster: list) -> None:
    """
    Gather tests and remove them from the modulo cluster
    :param data:                Test suite data from output.xml
    :param execution_times:     Dictionary where test names and their execution times are stored
    :param modulo_cluster:      Cluster containing the tests that aren't assigned yet
    :return:                    None
    """
    for suite in data.suite.suites:
        for test in suite.tests:

            if test.name in modulo_cluster:
                add_to_cluster_and_remove_from_modulo_cluster(execution_times, None, modulo_cluster, test)


def greedy_sort(execution_times: dict, time_clusters_names: list, timed_clusters: list) -> None:
    """
    Assigns tests to clusters in descending order.
    :param execution_times:         Dictionary where test names and their execution times are stored
    :param time_clusters_names:     Names of the tests only
    :param timed_clusters:          Times of the tests only
    :return:                        None
    """
    for test, time in dict(sorted(execution_times.items(), key=lambda x: x[1], reverse=True)).items():
        sum_per_cluster: list = [sum(timed_clusters) for timed_clusters in timed_clusters]
        index: int = sum_per_cluster.index(min(sum_per_cluster))
        timed_clusters[index].append(time)
        time_clusters_names[index].append(test)


def dependency_sort(dependency_cluster: list, file: dict, modulo_cluster: list, tags_cluster: list, test) -> None:
    """
    Sort into clusters based on dependencies
    :param dependency_cluster:  Cluster containing test cases with direct dependencies
    :param file:                File where dependencies are stored
    :param modulo_cluster:      Cluster where leftover test cases are stored
    :param tags_cluster:        Cluster where test cases with a tag mentioned in the dependency file are stored
    :param test:                The individual test to be sorted
    :return:                    None
    """
    found_in_dependency: bool = False
    found_in_tags = False

    for dependency_index in range(len(file["dependencies"])):

        if test.name in file["dependencies"][dependency_index]:
            add_to_cluster_and_remove_from_modulo_cluster(dependency_cluster, dependency_index, modulo_cluster, test)
            found_in_dependency = True

    for tags_index in range(len(file["tags"])):

        if file["tags"][tags_index] in test.tags and found_in_dependency is False and found_in_tags is False:
            add_to_cluster_and_remove_from_modulo_cluster(tags_cluster, tags_index, modulo_cluster, test)
            found_in_tags = True


def add_to_cluster_and_remove_from_modulo_cluster(cluster_group: list or dict, test_index: int or None,
                                                  modulo_cluster: list, test: robot.result.TestCase) -> None:
    """
    Add test to a new cluster group, and remove from the modulo cluster
    :param cluster_group:   Cluster group to be added to
    :param test_index:      Index of the cluster to be added to
    :param modulo_cluster:  Leftover test case group.
    :param test:            Test in question.
    :return:                None
    """
    if type(cluster_group) is dict:
        cluster_group[test.name] = (test.elapsedtime / 1000)
    else:
        cluster_group[test_index].append(test.name)
    modulo_cluster.remove(test.name)


def remove_empty_clusters(clusters: list) -> list:
    """
    Removes leftover clusters
    :param clusters:    Cluster group containing all clusters
    :return:            Clusters without empty clusters
    """
    return [cluster for cluster in clusters if len(cluster) != 0]


def generate_clusters(cluster_size: int or list) -> list:
    """
    Generate cluster groups within a cluster
    :param cluster_size:    The size of the group
    :return:                A cluster group with :var: cluster_size amount of clusters
    """
    if type(cluster_size) is int:
        return [[] for _ in range(cluster_size)]
    else:
        return [[] for _ in cluster_size]


def add_cluster_group_to_all_clusters(clusters: list, cluster_group: list) -> None:
    """
    Add a cluster group to the overarching cluster group
    :param clusters:        Overarching cluster group
    :param cluster_group:   Group to be added to :var: clusters
    :return:                :var: clusters
    """
    clusters.extend(cluster_group)


def retrieve_dry_run_results(suites_location: str) -> ExecutionResult:
    """
    Get the dry run results from Robot Test Suites
    :param suites_location:     where the suites are stored
    :return:                    A Robot object containing the execution results
    """
    return TestSuite.from_file_system(PurePath(suites_location)).run(dryrun=True, outputdir=PurePath("../dryrunlog"))


def extract_xml(output: str) -> ExecutionResult:
    """
    Extract data from the output.xml
    :param output:  name of the output_xml
    :return:        XML result
    """
    return ExecutionResult(PurePath(output), merge=False)
