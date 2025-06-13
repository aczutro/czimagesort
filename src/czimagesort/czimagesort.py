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
Application to easily sort images based on user preference.
"""

from .preferencesorter import PreferenceSorter

import argparse
import tkinter as tk


def main():
    parser = argparse.ArgumentParser(
        description="A tool to sort images by choosing from random pairs."
    )
    parser.add_argument(
        'files',
        metavar='FILE',
        type=str,
        nargs='+',
        help='One or more image files to be sorted.'
    )
    args = parser.parse_args()

    if not args.files:
        print("Error: No image files provided. Please specify at least one image file.")
        parser.print_help()
        return
    #if

    root = tk.Tk()
    PreferenceSorter(root, args.files)
    root.mainloop()
#main


### aczutro ###################################################################
