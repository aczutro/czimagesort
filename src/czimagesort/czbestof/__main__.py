# Copyright (C) 2025 - present  Alexander Czutro <github@czutro.ch>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# For more details, see the provided licence file or
# <http://www.gnu.org/licenses>.
#
################################################################### aczutro ###

"""
A tool to easily sort images based on user preference.
"""
import sys

from .. import __project__, __version__
from .preferencesorter import PreferenceSorter, PreferenceSorterError

from czutils.lib import czuioutput

import argparse
import logging


def _parseCommandLine(uiout: czuioutput.OutputChannel) -> list[str]:

    parser = argparse.ArgumentParser(
        description="A tool to easily sort images based on user preference."
    )
    parser.add_argument('files',
                        metavar='FILE',
                        type=str,
                        nargs='+',
                        help='Image file.',
                        )
    parser.add_argument("--version",
                        action="version",
                        version=f"{__project__} version {__version__}",
                        help="show version number and exit",
                        )
    args = parser.parse_args()

    if not args.files:
        uiout.error("No image files provided.")
        sys.exit(1)
    #if

    return args.files
#_parseCommandLine


def main():
    logging.basicConfig(level=logging.CRITICAL)
    uiout = czuioutput.OutputChannel()

    files = _parseCommandLine(uiout)
    try:
        sorter = PreferenceSorter(files, uiout)
        sorter.mainloop()
        sys.exit(0)
    except PreferenceSorterError as e:
        uiout.error(e)
        sys.exit(1)
    #except
#main


### aczutro ###################################################################
