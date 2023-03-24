import json


def generate_dependency_and_tags_clusters(file):
    dependency_cluster = [[] for _ in file["dependencies"]]
    tags_cluster = [[] for _ in file["tags"]]
    return dependency_cluster, tags_cluster


def retrieve_dependencies(dependency_file):
    file = json.load(open(dependency_file))
    return file