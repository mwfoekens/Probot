import sys

from robot import rebot
from pathlib import PurePath
import os
import shutil
import time
from datetime import datetime, timedelta

XML_LOCATION = "test-output"
OUTPUT_LOCATION = "output"


def combine_results(xml_location: str, output_location: str, start_and_end: tuple) -> None:
    """
    Combine the results with rebot.
    :param xml_location:        Location of where the individual test outputs are stored
    :param output_location:     Location of where the combined log should be stored
    :param start_and_end:     Runtime of longest cluster
    :return:                    None
    """
    output_xmls = [PurePath(f"{xml_location}/{file.name}") for file in os.scandir(PurePath(xml_location)) if
                   file.name.endswith(".xml")]

    rebot(*output_xmls,
          outputdir=PurePath(output_location),
          output=f"{TIMESTAMP}-output.xml",
          report=f"{TIMESTAMP}-report.html",
          log=f"{TIMESTAMP}-log.html",
          reporttitle="COMBINED REPORT",
          logtitle="COMBINED LOG",
          name="Combined Suites",
          starttime=start_and_end[0],
          endtime=start_and_end[1])


def copy_output_directory(xml_location: str, output_location: str, directory: str) -> None:
    """
    Copy an outputted directory to the output location, removes directory of the same name
    :param xml_location:    Location of where the individual test outputs are stored
    :param output_location: Location of where the combined log should be stored
    :param directory:       Name of directory
    :return:                None
    """
    complete_output_path = get_complete_path(output_location, directory)
    complete_xml_path = get_complete_path(xml_location, directory)
    if os.path.exists(complete_output_path) and os.path.exists(complete_xml_path):
        shutil.rmtree(complete_output_path)
        shutil.copytree(complete_xml_path, complete_output_path)

    if not os.path.exists(complete_output_path) and os.path.exists(complete_xml_path):
        shutil.copytree(complete_xml_path, complete_output_path)


def copy_output_file(xml_location: str, output_location: str, file: str) -> None:
    """
    Copy an outputted file to the output location, removes file of the same name
    :param xml_location:    Location of where the individual test outputs are stored
    :param output_location: Location of where the combined log should be stored
    :param file:            Name of file
    :return:                None
    """
    complete_output_path = get_complete_path(output_location, file)
    complete_xml_path = get_complete_path(xml_location, file)
    if os.path.exists(complete_output_path) and os.path.exists(complete_xml_path):

        os.remove(complete_output_path)
        shutil.copy(complete_xml_path, complete_output_path)

    elif not os.path.exists(complete_output_path) and os.path.exists(complete_xml_path):
        shutil.copy(complete_xml_path, complete_output_path)


def get_complete_path(path: str, item: str):
    """
    Get complete path of a file or directory
    :param path:    Prefix path of the item.
    :param item:    May be a file or directory.
    :return:        Complete path
    """
    return PurePath(f"{path}/{item}")


def get_longest_running_cluster(xml_location: str) -> tuple:
    """
    Get the name and time of the cluster that ran the longest
    :param xml_location:    location of the output files
    :return:                Name of the longest cluster, time of the longest cluster
    """
    time_files = [file for file in os.scandir(PurePath(xml_location)) if file.name.endswith("runtime.txt")]
    times = dict()

    for file in time_files:
        with open(file, "r") as f:
            times[file.name] = float(f.readline())

    times = sorted(times.items(), key=lambda x: x[1], reverse=True)

    return times[0][0].split("-")[0], times[0][1]


def get_start_and_end_times(runtime: float) -> tuple:
    """
    Get the start and end times of a test suite based on the longest runtime
    :param runtime: The longest runtime
    :return:        Start and end
    """
    end = datetime.now()
    start = end - timedelta(seconds=runtime)
    return start.strftime("%Y%m%d %H:%M:%S.%f"), end.strftime("%Y%m%d %H:%M:%S.%f")


if __name__ == '__main__':

    if any(os.scandir(PurePath(XML_LOCATION))):
        TIMESTAMP = str(time.strftime("%Y-%m-%d_%H.%M.%S"))
        longest_runtime_name, longest_runtime = get_longest_running_cluster(XML_LOCATION)
        print(f"Longest running executor was {longest_runtime_name} with {longest_runtime} seconds")
        combine_results(XML_LOCATION, OUTPUT_LOCATION, get_start_and_end_times(longest_runtime))

    else:
        print("No log files found.")
        sys.exit(1)

    # Only copy the browser folder/playwright log if there's actually a log file created.
    # Otherwise the log combiner pod was too fast, and needs to wait.
    if os.path.exists(PurePath(f"{OUTPUT_LOCATION}/{TIMESTAMP}-log.html")):
        copy_output_directory(XML_LOCATION, OUTPUT_LOCATION, "browser")
        copy_output_file(XML_LOCATION, OUTPUT_LOCATION, "playwright-log.txt")
        sys.exit(0)

    print("Not ready.")
    sys.exit(1)
