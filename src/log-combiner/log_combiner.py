from robot import rebot
from pathlib import PurePath
import os
import shutil

XML_LOCATION = "test-output"
OUTPUT_LOCATION = "output"


def combine_results(xml_location: str, output_location: str):
    rebot(*[PurePath(f"{xml_location}/{file.name}") for file in os.scandir(PurePath(xml_location)) if
            file.name.endswith(".xml")], outputdir=PurePath(output_location), output="output.xml",
          reporttitle="COMBINED LOG", logtitle="COMBINED LOG")


def move_output_items(xml_location: str, output_location: str, item: str):
    if os.path.exists(PurePath(f"{output_location}/{item}")):
        shutil.rmtree(PurePath(f"{output_location}/{item}"))
    shutil.copytree(PurePath(f"{xml_location}/{item}"), PurePath(f"{output_location}/{item}"))


combine_results(XML_LOCATION, OUTPUT_LOCATION)
move_output_items(XML_LOCATION, OUTPUT_LOCATION, "browser")
move_output_items(XML_LOCATION, OUTPUT_LOCATION, "playwright-log.txt")
