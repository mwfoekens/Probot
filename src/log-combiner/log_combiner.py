import sys

from robot import rebot
from pathlib import PurePath
import os
import shutil
import time

XML_LOCATION = "test-output"
OUTPUT_LOCATION = "output"


def combine_results(xml_location: str, output_location: str, longest_runtime: str) -> None:
    """
    Combine the results with rebot.
    :param xml_location:        Location of where the individual test outputs are stored
    :param output_location:     Location of where the combined log should be stored
    :param longest_runtime:     Runtime of longest cluster
    :return:                    None
    """
    if any(os.scandir(PurePath(xml_location))):

        output_xmls = [PurePath(f"{xml_location}/{file.name}") for file in os.scandir(PurePath(xml_location)) if
                       file.name.endswith(".xml")]
        rebot(*output_xmls,
              outputdir=PurePath(output_location),
              output=f"{TIMESTAMP}-output.xml",
              report=f"{TIMESTAMP}-report.html",
              log=f"{TIMESTAMP}-log.html",
              reporttitle="COMBINED REPORT",
              logtitle="COMBINED LOG",
              name="Combined Suites")

    else:
        print("No log files found.")
        sys.exit(1)


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


def get_longest_running_cluster(xml_location):
    time_files = [file for file in os.scandir(PurePath(xml_location)) if file.name.endswith("runtime.txt")]
    times = []
    for file in time_files:
        with open(file, "r") as f:
            times.append(float(f.readline()))

    longest = sorted(times, reverse=True)[0]
    return '{0:02.0f}:{1:02.0f}'.format(*divmod(longest * 60, 60))


TIMESTAMP = str(time.strftime("%Y-%m-%d_%H.%M.%S"))
longest_runtime = get_longest_running_cluster(XML_LOCATION)
combine_results(XML_LOCATION, OUTPUT_LOCATION, longest_runtime)

# Only copy the browser folder/playwright log if there's actually a log file created.
# Otherwise the log combiner pod was too fast, and needs to wait.
if os.path.exists(PurePath(f"{OUTPUT_LOCATION}/{TIMESTAMP}-log.html")):
    copy_output_directory(XML_LOCATION, OUTPUT_LOCATION, "browser")
    copy_output_file(XML_LOCATION, OUTPUT_LOCATION, "playwright-log.txt")
    sys.exit(0)

print("Not ready.")
sys.exit(1)
