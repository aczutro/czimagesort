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
Image classifier based on user preference.
"""

from ..common import utils
from .conf import *

from czutils.lib import czuioutput

import random
import tkinter as tk
import tkinter.messagebox as tkmessagebox
from tkinter import font as tkfont


class PreferenceSorterError(Exception):
    pass
#PreferenceSorterError


class PreferenceSorter(tk.Tk):
    """
    A GUI application to display images pair-wise for manual sorting.
    The user can choose one image, the other, or neither. The files are then
    moved to 'chosen' or 'discarded' directories.
    """

    def __init__(self,
                 imageFiles: list[str],
                 uiout: czuioutput.OutputChannel,
                 ):
        """
        Args:
            imageFiles (list): A list of paths to the image files.
        """
        super().__init__()

        self.title("czimagesort - choose your favourite")
        self.configure(bg=BG_COLOUR)

        self.imageList = utils.filterValidImages(imageFiles, uiout.warning)
        if not self.imageList:
            tk.messagebox.showinfo("No Valid Images",
                                   "No valid image files found.")
            raise PreferenceSorterError("No valid image files found.")
        #if

        random.shuffle(self.imageList)

        self._displayImage = lambda l, i: utils.displayImage(label=l,
                                                             image=i,
                                                             width=IMAGE_DISPLAY_SIZE[0],
                                                             height=IMAGE_DISPLAY_SIZE[1],
                                                             bgColour=BG_COLOUR,
                                                             )
        self._moveFile = lambda f, d: utils.moveFile(srcPath=Path(f),
                                                     destDir=Path(d),
                                                     infoFn=uiout.info,
                                                     errorFn=uiout.error,
                                                     )

        self._currentIndex = 0

        self._leftImagePath = None
        self._rightImagePath = None

        self._setupDirectories()
        self._setupUI()

        self._loadNextPair()
    #__init__


    def _setupDirectories(self):
        """
        Creates the '.chosen' and '.discarded' directories if they don't exist.
        """
        isinstance(self, PreferenceSorter)
        try:
            CHOSEN_DIR.mkdir(parents=True, exist_ok=True)
            DISCARDED_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            tk.messagebox.showerror("Error", f"Failed to create output directories.")
            raise PreferenceSorterError(f"Failed to create output directories: {e}")
        #except
    #_setupDirectories


    def _setupUI(self):
        """
        Creates and arranges the widgets in the tkinter window.
        """
        mainFrame = tk.Frame(self, bg=BG_COLOUR, padx=PADDING, pady=PADDING)
        mainFrame.pack(expand=True, fill=tk.BOTH)

        imageFrame = tk.Frame(mainFrame, bg=BG_COLOUR)
        imageFrame.pack(padx=0, pady=0, expand=True, fill=tk.BOTH)

        self.labelLeft = tk.Label(imageFrame, bg=BG_COLOUR, relief=tk.RAISED, borderwidth=2)
        self.labelLeft.pack(side=tk.LEFT, padx=PADDING, pady=PADDING, expand=True, fill=tk.BOTH)
        self.labelLeft.bind("<Button-1>", lambda e: self._handleChoice("left"))

        self.labelRight = tk.Label(imageFrame, bg=BG_COLOUR, relief=tk.RAISED, borderwidth=2)
        self.labelRight.pack(side=tk.RIGHT, padx=PADDING, pady=PADDING, expand=True, fill=tk.BOTH)
        self.labelRight.bind("<Button-1>", lambda e: self._handleChoice("right"))

        controlFrame = tk.Frame(mainFrame, bg=BG_COLOUR)
        controlFrame.pack(pady=PADDING)

        defaultFont = tkfont.nametofont("TkDefaultFont")
        self.neitherButton = tk.Button(
            controlFrame,
            text="neither",
            command=lambda: self._handleChoice("neither"),
            bg="red",
            fg="white",
            font=(defaultFont.actual("family"), defaultFont.actual("size"), "bold"),
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=5
        )
        self.neitherButton.pack()

        offset = self.winfo_screenwidth() - self.winfo_width()
        self.geometry(f"+{offset}+0")
    #_setupUI


    def _loadNextPair(self):
        """
        Loads the next pair of images, or the final single image.
        """
        if self._currentIndex + 1 < len(self.imageList):

            self._leftImagePath = self.imageList[self._currentIndex]
            self._rightImagePath = self.imageList[self._currentIndex + 1]

            self._displayImage(self.labelLeft, self._leftImagePath)
            self._displayImage(self.labelRight, self._rightImagePath)

        elif self._currentIndex < len(self.imageList):

            self._leftImagePath = self.imageList[self._currentIndex]
            self._rightImagePath = None

            self._displayImage(self.labelLeft, self._leftImagePath)

            self.labelRight.config(image="",
                                   text="     no image     ",
                                   fg="#cccccc",
                                   )
            self.labelRight.image = None
            self.labelRight.unbind("<Button-1>")

            self.labelLeft.unbind("<Button-1>")
            self.labelLeft.bind("<Button-1>",
                                lambda e: self._handleLastImageChoice(choose=True),
                                )

            self.neitherButton.config(text="discard",
                                      command=lambda: self._handleLastImageChoice(choose=False),
                                      )

        else:
            self.quit()
        #else
    #_loadNextPair


    def _handleChoice(self, choice: str):
        """
        Handles the user's choice for a pair by moving files and loading the next pair.
        Args:
            choice (str): 'left', 'right', or 'neither'.
        """
        if not self._leftImagePath or not self._rightImagePath:
            return
        #if

        try:
            if choice == 'left':
                self._moveFile(self._leftImagePath, CHOSEN_DIR)
                self._moveFile(self._rightImagePath, DISCARDED_DIR)
            elif choice == 'right':
                self._moveFile(self._rightImagePath, CHOSEN_DIR)
                self._moveFile(self._leftImagePath, DISCARDED_DIR)
            elif choice == 'neither':
                self._moveFile(self._leftImagePath, DISCARDED_DIR)
                self._moveFile(self._rightImagePath, DISCARDED_DIR)
            #elif

            self._currentIndex += 2
            self._loadNextPair()

        except OSError as e:
            tk.messagebox.showerror("File Error", f"Couldn't move files.")
            raise PreferenceSorterError(f"Couldn't move files: {e}")
        #except
    #_handleChoice


    def _handleLastImageChoice(self, choose):
        """
        Handles the final choice for the last remaining image.
        Args:
            choose (bool): True if the image is chosen, False if discarded.
        """
        if not self._leftImagePath:
            return
        #if

        try:
            if choose:
                self._moveFile(self._leftImagePath, CHOSEN_DIR)
            else:
                self._moveFile(self._leftImagePath, DISCARDED_DIR)
            #else

            self._currentIndex += 1
            self._loadNextPair()

        except OSError as e:
            tk.messagebox.showerror("File Error", f"Couldn't move files.")
            raise PreferenceSorterError(f"Couldn't move files: {e}")
        #except
    #_handleLastImageChoice

#class PreferenceSorter


### aczutro ###################################################################
