import robot.api
from robot.api import TestSuite, ExecutionResult
from random import choice

from dependency import *


# if we have a dependency file, we read the tags and dependencies and store that info
# then we get the test suite info from a robot --dryrun
# we go through the test suites and if the test is in dependencies/tags, we add to their clusters
# else we check if it exists in the output XML
# else we put it in a random cluster
# send all clusters to the queue (rabbitMQ?)

# docker does its thing and runs all clusters

# all report snippets get assembled into one report
# success

def main(dependency_file=None, output=None, time_cluster_size=5, random_cluster_size=5):
    clusters: list = []
    modulo_cluster: list = []

    if dependency_file is not None:
        file: json = retrieve_dependencies(dependency_file)
        dependency_cluster, tags_cluster = generate_dependency_and_tags_clusters(file)
    else:
        print("No dependency.json found.")

    result: robot.api.ExecutionResult = retrieve_dry_run_results()

    for suite in result.suite.suites:
        for test in suite.tests:
            modulo_cluster.append(test.name)

            if dependency_file is not None:
                dependency_sort(dependency_cluster, file, modulo_cluster, tags_cluster, test)

    if dependency_file is not None:
        add_cluster_group_to_all_clusters(clusters, dependency_cluster)
        add_cluster_group_to_all_clusters(clusters, tags_cluster)

    if output is not None:
        outputxml_sort(clusters, modulo_cluster, output, time_cluster_size)
    else:
        print("No output.xml")

    # Then we assign randomly, because we just dont have that data.
    add_cluster_group_to_all_clusters(clusters, random_sort(modulo_cluster, random_cluster_size))

    clusters: list = remove_empty_clusters(clusters)

    return clusters


def random_sort(modulo_cluster, random_cluster_size):
    random_clusters: list = generate_clusters(random_cluster_size)
    for test in modulo_cluster:
        choice(random_clusters).append(test)
    return random_clusters


def outputxml_sort(clusters, modulo_cluster, output, time_cluster_size):
    # Then we check whether we got an output.xml file, we read that too
    execution_times: dict = dict()
    data: ExecutionResult = ExecutionResult(output, merge=False)

    for suite in data.suite.suites:
        for test in suite.tests:

            if test.name in modulo_cluster:
                execution_times[test.name] = (test.elapsedtime / 1000)
                modulo_cluster.remove(test.name)

    sorted_execution_times: dict = dict(sorted(execution_times.items(), key=lambda x: x[1], reverse=True))
    timed_clusters: list = generate_clusters(time_cluster_size)
    time_clusters_names: list = generate_clusters(time_cluster_size)

    for test, time in sorted_execution_times.items():

        sum_per_cluster: list = [sum(timed_clusters) for timed_clusters in timed_clusters]
        index: int = sum_per_cluster.index(min(sum_per_cluster))
        timed_clusters[index].append(time)
        time_clusters_names[index].append(test)

    add_cluster_group_to_all_clusters(clusters, time_clusters_names)


def dependency_sort(dependency_cluster, file, modulo_cluster, tags_cluster, test):
    found_in_dependency: bool = False

    for i in range(len(file["dependencies"])):
        if test.name in file["dependencies"][i]:
            add_to_cluster_and_remove_from_modulo_cluster(dependency_cluster, i, modulo_cluster, test)
            found_in_dependency = True

    for i in range(len(file["tags"])):
        if file["tags"][i] in test.tags and found_in_dependency is False:
            add_to_cluster_and_remove_from_modulo_cluster(tags_cluster, i, modulo_cluster, test)


def add_to_cluster_and_remove_from_modulo_cluster(cluster_group, i, modulo_cluster, test):
    cluster_group[i].append(test.name)
    modulo_cluster.remove(test.name)


def remove_empty_clusters(clusters):
    return [cluster for cluster in clusters if len(cluster) != 0]


def generate_clusters(cluster_size):
    return [[] for _ in range(cluster_size)]


def add_cluster_group_to_all_clusters(clusters, cluster_group):
    clusters.extend(cluster_group)


def retrieve_dry_run_results() -> robot.api.ExecutionResult:
    return TestSuite.from_file_system("").run(dryrun=True)


res = main("dependency.json", "log\\output.xml", time_cluster_size=2)
print(f"clusters: {res}")
