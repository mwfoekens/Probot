from robot import rebot
from pathlib import PurePath
import os
import shutil

XML_LOCATION = "test-output"
OUTPUT_LOCATION = "output"


def combine_results(xml_location: str, output_location: str):
    rebot(*[PurePath(f"{xml_location}/{file.name}") for file in os.scandir(PurePath(xml_location)) if
            file.name.endswith(".xml")], outputdir=PurePath(output_location), output="output.xml",
          reporttitle="COMBINED REPORT", logtitle="COMBINED LOG")


def copy_output_dirs(xml_location: str, output_location: str, dir: str):
    if os.path.exists(PurePath(f"{output_location}/{dir}")):
        shutil.rmtree(PurePath(f"{output_location}/{dir}"))
    shutil.copytree(PurePath(f"{xml_location}/{dir}"), PurePath(f"{output_location}/{dir}"))


def copy_output_files(xml_location: str, output_location: str, file: str):
    if os.path.exists(PurePath(f"{output_location}/{file}")):
        os.remove(PurePath(f"{output_location}/{dir}"))
    shutil.copy(PurePath(f"{xml_location}/{file}"), PurePath(f"{output_location}/{file}"))


combine_results(XML_LOCATION, OUTPUT_LOCATION)
copy_output_dirs(XML_LOCATION, OUTPUT_LOCATION, "browser")
copy_output_files(XML_LOCATION, OUTPUT_LOCATION, "playwright-log.txt")
