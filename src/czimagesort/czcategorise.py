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
A tool to sort images into multiple categories.
"""

from .categorysorter import CategorySorter

import argparse
import importlib.metadata
import json
import os
import tkinter as tk


def loadConfig(configPath):
    """
    Loads the configuration file.
    """
    if not os.path.exists(configPath):
        defaultConfig = {
            "categories": [
                {
                    "label": "Nature",
                    "directory": ".nature",
                    "shortcut": "n"
                },
                {
                    "label": "People",
                    "directory": ".people",
                    "shortcut": "p"
                },
                {
                    "label": "Archive",
                    "directory": ".archive",
                    "shortcut": "a"
                }
            ],
            "skip_shortcut": "space"
        }

        with open(configPath, 'w') as f:
            json.dump(defaultConfig, f, indent=4)
        #with

        print(f"Default config file '{configPath}' created.  Edit it first.")
        return None
    #if

    with open(configPath, 'r') as f:
        return json.load(f)
    #with
#loadConfig


def main():
    metadata = importlib.metadata.distribution(__package__).metadata

    parser = argparse.ArgumentParser(
        description="A tool to sort images into multiple categories."
    )
    parser.add_argument(
        'files',
        metavar='FILE',
        type=str,
        nargs='+',
        help='One or more image files to be sorted.'
    )
    parser.add_argument("--version",
                        action="version",
                        version=f"{metadata['Name']} {metadata['Version']}",
                        help="show version number and exit")
    args = parser.parse_args()

    if not args.files:
        print("Error: No image files provided. Please specify at least one image file.")
        parser.print_help()
        return
    #if

    config = loadConfig(f"{os.path.expanduser('~')}/.config/{__name__}.json")
    if not config:
        return
    #if

    root = tk.Tk()
    CategorySorter(root, args.files, config)
    root.mainloop()
    root.mainloop()
#main


### aczutro ###################################################################
