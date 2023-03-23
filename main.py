import json
from pprint import pprint
from robot.api import TestSuite, ExecutionResult
from random import choice

from dependency import *


def main(dependency_file=None, output=None, time_cluster_size=5, random_cluster_size=5):
    # if we have a dependency file, we read the tags and dependencies and store that info
    # then we get the test suite info from a robot --dryrun
    # we go through the test suites and if the test is in dependencies/tags, we add to their clusters
    # else we check if it exists in the output XML
    # else we put it in a random cluster
    # send all clusters to the queue (rabbitMQ?)

    # docker does its thing and runs all clusters

    # all report snippets get assembled into one report
    # success

    clusters = []
    modulo_cluster = []

    if dependency_file is not None:
        file = retrieve_json_data(dependency_file)
        dependency_cluster, tags_cluster = generate_dependency_and_tags_clusters(file)
    else:
        print("No dependency.json found.")

    result = retrieve_test_suite_results()

    for test in result.suite.tests._items:
        modulo_cluster.append(test.name)
        found_in_dependency = False

        if dependency_file is not None:
            for i in range(len(file["dependencies"])):

                if test.name in file["dependencies"][i]:
                    add_to_cluster_and_remove_from_modulo_cluster(dependency_cluster, i, modulo_cluster, test)
                    found_in_dependency = True

            for i in range(len(file["tags"])):

                if file["tags"][i] in test.tags and found_in_dependency is False:
                    add_to_cluster_and_remove_from_modulo_cluster(tags_cluster, i, modulo_cluster, test)

    if dependency_file is not None:
        add_cluster_group_to_all_clusters(clusters, dependency_cluster)
        add_cluster_group_to_all_clusters(clusters, tags_cluster)

    if output is not None:
        # Then we check whether we got an output.xml file, we read that too
        execution_times = dict()
        timed_clusters = generate_dependency_and_tags_clusters(time_cluster_size)
        data = ExecutionResult(output, merge=False)
        for test in data.suite.tests:

            if test.name in modulo_cluster:
                execution_times[test.name] = (test.elapsedtime / 1000)
                modulo_cluster.remove(test.name)

        sorted_execution_times = dict(sorted(execution_times.items(), key=lambda x: x[1], reverse=True))

        for test, time in sorted_execution_times.items():
            sum_per_cluster = [sum(timed_clusters) for timed_clusters in timed_clusters]
            index = sum_per_cluster.index(min(sum_per_cluster))
            timed_clusters[index].append(test)

        add_cluster_group_to_all_clusters(clusters, timed_clusters)
    else:
        print("No output.xml")

    # Then we assign randomly, because we just dont have that data.
    random_clusters = generate_dependency_and_tags_clusters(random_cluster_size)
    for test in modulo_cluster:
        choice(random_clusters).append(test)

    add_cluster_group_to_all_clusters(clusters, random_clusters)

    clusters = remove_empty_clusters(clusters)

    print(f"Clusters: {clusters}")


def add_to_cluster_and_remove_from_modulo_cluster(cluster_group, i, modulo_cluster, test):
    cluster_group[i].append(test.name)
    modulo_cluster.remove(test.name)


def remove_empty_clusters(clusters):
    return [cluster for cluster in clusters if len(cluster) != 0]


def generate_clusters(cluster_size):
    return [[] for _ in range(cluster_size)]


def add_cluster_group_to_all_clusters(clusters, cluster_group):
    clusters.extend(cluster_group)


def retrieve_test_suite_results():
    test_suite = TestSuite.from_file_system("test.robot")
    return test_suite.run(dryrun=True)


main("dependency.json", "log\\output.xml")
