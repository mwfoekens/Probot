from robot import rebot
from pathlib import PurePath
import os
import shutil

XML_LOCATION = "test-output"
OUTPUT_LOCATION = "output"


def combine_results(xml_location: str, output_location: str) -> None:
    """
    Combine the results with rebot.
    :param xml_location:        Location of where the individual test outputs are stored
    :param output_location:     Location of where the combined log should be stored
    :return:                    None
    """
    if any(os.scandir(PurePath(xml_location))):
        rebot(*[PurePath(f"{xml_location}/{file.name}") for file in os.scandir(PurePath(xml_location)) if
                file.name.endswith(".xml")], outputdir=PurePath(output_location), output="output.xml",
              reporttitle="COMBINED REPORT", logtitle="COMBINED LOG")


def copy_output_directory(xml_location: str, output_location: str, directory: str) -> None:
    """
    Copy an outputted directory to the output location, removes directory of the same name
    :param xml_location:    Location of where the individual test outputs are stored
    :param output_location: Location of where the combined log should be stored
    :param directory:       Name of directory
    :return:                None
    """
    complete_output_path = PurePath(f"{output_location}/{directory}")
    complete_xml_path = PurePath(f"{xml_location}/{directory}")
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
    complete_output_path = PurePath(f"{output_location}/{file}")
    complete_xml_path = PurePath(f"{xml_location}/{file}")
    if os.path.exists(complete_output_path) and os.path.exists(complete_xml_path):

        os.remove(complete_output_path)
        shutil.copy(complete_xml_path, complete_output_path)

    elif not os.path.exists(complete_output_path) and os.path.exists(complete_xml_path):
        shutil.copy(complete_xml_path, complete_output_path)


combine_results(XML_LOCATION, OUTPUT_LOCATION)
copy_output_directory(XML_LOCATION, OUTPUT_LOCATION, "browser")
copy_output_file(XML_LOCATION, OUTPUT_LOCATION, "playwright-log.txt")
