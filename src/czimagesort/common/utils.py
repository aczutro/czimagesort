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
Help functions.
"""

from PIL import Image, ImageTk, UnidentifiedImageError
import logging
from pathlib import Path
import shutil
import tkinter as tk
from typing import Callable


_logger = logging.getLogger(__name__)


def filterValidImages(files: list[str],
                      warningFn : Callable[[str], None],
                      ):
    """
    Filters a list of files to include only valid, readable images.
    """
    validImages = []
    for f in files:
        try:
            img = Image.open(f)
            img.verify()
            validImages.append(f)
        except (IOError, SyntaxError, UnidentifiedImageError) as e:
            warningFn(f"skipping '{f}': {e}")
        #except
    return validImages
#filterValidImages


def displayImage(label: tk.Label,
                 image: Path | str,
                 width: int,
                 height: int,
                 bgColour: str
                 ):
    """
    Opens, resizes, and displays an image in a given label.
    """
    imagePath = Path(image)

    try:
        img = Image.open(imagePath)
        img.thumbnail((width, height), Image.Resampling.LANCZOS)

        bgImg = Image.new('RGB', (width, height), bgColour)
        bgImg.paste(img,
                    ((width - img.width) // 2,
                     (height - img.height) // 2,
                     ),
                    )

        photoImg = ImageTk.PhotoImage(bgImg)

        label.config(image=photoImg)
        label.image = photoImg

    except (IOError, UnidentifiedImageError) as e:
        label.config(text=f"Failed to display '{imagePath.name}'",
                     image='',
                     justify=tk.CENTER,
                     fg='red',
                     )
        _logger.error(f"Failed to display '{imagePath}': {e}")
    #except
#displayImage


def moveFile(srcPath: Path,
             destDir: Path,
             infoFn : Callable[[str], None],
             errorFn : Callable[[str], None],
             ):
    """
    Moves a file and prints the action to the console.
    """
    try:
        if srcPath.exists():
            fileName = srcPath.name
            destPath = destDir / fileName
            shutil.move(srcPath, destPath)
            infoFn(f"'{srcPath}' --> '{destDir}'")
        else:
            _logger.warning(f"cannot move file '{srcPath}': not found")
        #else
    except (shutil.Error, IOError) as e:
        errorFn(f"Failed to move '{srcPath}': {e}")
    #except

#moveFile


### aczutro ###################################################################
