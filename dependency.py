import json


def generate_dependency_and_tags_clusters(file):
    return [[] for _ in file["dependencies"]], [[] for _ in file["tags"]]


def retrieve_dependencies(dependency_file):
    return json.load(open(dependency_file))
