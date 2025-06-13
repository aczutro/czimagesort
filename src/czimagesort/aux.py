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
Auxiliary functions.
"""

from .conf import *

from PIL import Image, ImageTk, UnidentifiedImageError
import os
import shutil
import tkinter as tk


def filterValidImages(files):
    """
    Filters a list of files to include only valid, readable images.
    """
    validImages = []
    for f in files:
        try:
            img = Image.open(f)
            img.verify()
            validImages.append(f)
        except (IOError, SyntaxError, UnidentifiedImageError):
            print(f"Warning: Skipping invalid or corrupt image file: {f}")
        #except
    return validImages
#filterValidImages


def displayImage(label, imagePath):
    """
    Opens, resizes, and displays an image in a given label.
    """
    try:
        img = Image.open(imagePath)
        img.thumbnail(IMAGE_DISPLAY_SIZE, Image.Resampling.LANCZOS)

        bgImg = Image.new('RGB', IMAGE_DISPLAY_SIZE, BG_COLOUR)
        bgImg.paste(img,
                    ((IMAGE_DISPLAY_SIZE[0] - img.width) // 2,
                     (IMAGE_DISPLAY_SIZE[1] - img.height) // 2))

        photoImg = ImageTk.PhotoImage(bgImg)

        label.config(image=photoImg)
        label.image = photoImg
    except (IOError, UnidentifiedImageError) as e:
        label.config(text=f"Error loading:\n{os.path.basename(imagePath)}",
                     image='',
                     justify=tk.CENTER,
                     fg='red')
        print(f"Error displaying image {imagePath}: {e}")
    #except
#displayImage


def moveFile(srcPath, destDir):
    """
    Moves a file and prints the action to the console.
    """
    try:
        if os.path.exists(srcPath):
            file_name = os.path.basename(srcPath)
            dest_path = os.path.join(destDir, file_name)
            shutil.move(srcPath, dest_path)
            print(f"'{file_name}' --> '{destDir}'")
        else:
            print(f"Warning: Source file not found, cannot move: {srcPath}")
        #else
    except shutil.Error as e:
        print(f"Could not move file {srcPath}. Reason: {e}")
    except Exception as e:
        print(f"An unexpected error occurred moving {srcPath}: {e}")
    #except
#moveFile


### aczutro ###################################################################
