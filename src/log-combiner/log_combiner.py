from robot import rebot
from pathlib import PurePath
import os


def combine_results(xml_location, output_location):
    rebot(*[PurePath(f"{xml_location}/{file.name}") for file in os.scandir(PurePath(xml_location))],
          outputdir=PurePath(output_location), output="output.xml", reporttitle="COMBINED LOG", logtitle="COMBINED LOG")


combine_results("test-output", "output")
