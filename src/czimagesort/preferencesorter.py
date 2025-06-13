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

from . import aux
from .conf import *

import os
import random
import tkinter as tk
import tkinter.messagebox
from tkinter import font as tkfont


class PreferenceSorter:
    """
    A GUI application to display images pair-wise for manual sorting.
    The user can choose one image, the other, or neither. The files are then
    moved to '.chosen' or '.discarded' directories.
    """

    def __init__(self, root, imageFiles):
        """
        Initializes the application, sets up the UI, and loads the first pair.
        Args:
            root: The root tkinter window.
            imageFiles (list): A list of paths to the image files.
        """
        self.root = root
        self.root.title("czimagesort - choose your favourite")
        self.root.configure(bg=BG_COLOUR)

        self.imageList = aux.filterValidImages(imageFiles)
        if not self.imageList:
            tk.messagebox.showinfo("No Valid Images",
                                   "No valid image files were found to process.")
            self.root.quit()
            return
        #if

        random.shuffle(self.imageList)

        self.currentIndex = 0

        self.leftImagePath = None
        self.rightImagePath = None

        self._setupDirectories()
        self._setupUI()

        self._loadNextPair()
    #__init__


    def _setupDirectories(self):
        """
        Creates the '.chosen' and '.discarded' directories if they don't exist.
        """
        try:
            os.makedirs(CHOSEN_DIR, exist_ok=True)
            os.makedirs(DISCARDED_DIR, exist_ok=True)
        except OSError as e:
            tk.messagebox.showerror("Error", f"Failed to create directories: {e}")
            self.root.quit()
        #except
    #_setupDirectories


    def _setupUI(self):
        """
        Creates and arranges the widgets in the tkinter window.
        """
        mainFrame = tk.Frame(self.root, bg=BG_COLOUR, padx=PADDING, pady=PADDING)
        mainFrame.pack(expand=True, fill=tk.BOTH)

        imageFrame = tk.Frame(mainFrame, bg=BG_COLOUR)
        imageFrame.pack(padx=0, pady=0, expand=True, fill=tk.BOTH)

        self.labelLeft = tk.Label(imageFrame, bg=BG_COLOUR, relief=tk.RAISED, borderwidth=2)
        self.labelLeft.pack(side=tk.LEFT, padx=PADDING, pady=PADDING, expand=True, fill=tk.BOTH)
        self.labelLeft.bind("<Button-1>", lambda e: self._handleChoice('left'))

        self.labelRight = tk.Label(imageFrame, bg=BG_COLOUR, relief=tk.RAISED, borderwidth=2)
        self.labelRight.pack(side=tk.RIGHT, padx=PADDING, pady=PADDING, expand=True, fill=tk.BOTH)
        self.labelRight.bind("<Button-1>", lambda e: self._handleChoice('right'))

        controlFrame = tk.Frame(mainFrame, bg=BG_COLOUR)
        controlFrame.pack(pady=PADDING)

        defaultFont = tkfont.nametofont("TkDefaultFont")
        self.neitherButton = tk.Button(
            controlFrame,
            text="neither",
            command=lambda: self._handleChoice('neither'),
            bg='red',
            fg='white',
            font=(defaultFont.actual('family'), defaultFont.actual('size'), 'bold'),
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=5
        )
        self.neitherButton.pack()

        offset = self.root.winfo_screenwidth() - self.root.winfo_width()
        self.root.geometry(f"+{offset}+0")
    #_setupUI


    def _loadNextPair(self):
        """
        Loads the next pair of images, or the final single image.
        """
        if self.currentIndex + 1 < len(self.imageList):

            self.leftImagePath = self.imageList[self.currentIndex]
            self.rightImagePath = self.imageList[self.currentIndex + 1]

            aux.displayImage(self.labelLeft, self.leftImagePath)
            aux.displayImage(self.labelRight, self.rightImagePath)

        elif self.currentIndex < len(self.imageList):

            self.leftImagePath = self.imageList[self.currentIndex]
            self.rightImagePath = None

            aux.displayImage(self.labelLeft, self.leftImagePath)

            self.labelRight.config(image='', text='     no image     ', fg='#cccccc')
            self.labelRight.image = None
            self.labelRight.unbind("<Button-1>")

            self.labelLeft.unbind("<Button-1>")
            self.labelLeft.bind("<Button-1>", lambda e: self._handleLastImageChoice(choose=True))

            self.neitherButton.config(text="discard",
                                      command=lambda: self._handleLastImageChoice(choose=False))

        else:
            self.root.quit()
        #else
    #_loadNextPair


    def _handleChoice(self, choice):
        """
        Handles the user's choice for a pair by moving files and loading the next pair.
        Args:
            choice (str): 'left', 'right', or 'neither'.
        """
        if not self.leftImagePath or not self.rightImagePath:
            return
        #if

        try:
            if choice == 'left':
                aux.moveFile(self.leftImagePath, CHOSEN_DIR)
                aux.moveFile(self.rightImagePath, DISCARDED_DIR)
            elif choice == 'right':
                aux.moveFile(self.rightImagePath, CHOSEN_DIR)
                aux.moveFile(self.leftImagePath, DISCARDED_DIR)
            elif choice == 'neither':
                aux.moveFile(self.leftImagePath, DISCARDED_DIR)
                aux.moveFile(self.rightImagePath, DISCARDED_DIR)
            #elif

            self.currentIndex += 2
            self._loadNextPair()

        except Exception as e:
            tk.messagebox.showerror("File Error",
                                    f"An error occurred while moving files: {e}")
            self.root.quit()
        #except
    #_handleChoice


    def _handleLastImageChoice(self, choose):
        """
        Handles the final choice for the last remaining image.
        Args:
            choose (bool): True if the image is chosen, False if discarded.
        """
        if not self.leftImagePath:
            return
        #if

        try:
            if choose:
                aux.moveFile(self.leftImagePath, CHOSEN_DIR)
            else:
                aux.moveFile(self.leftImagePath, DISCARDED_DIR)
            #else

            self.currentIndex += 1
            self._loadNextPair()

        except Exception as e:
            tk.messagebox.showerror("File Error",
                                    f"An error occurred while moving the last file: {e}")
            self.root.quit()
        #except
    #_handleLastImageChoice

#class PreferenceSorter


### aczutro ###################################################################
