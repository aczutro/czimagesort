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
Image classifier based on configurable categories.
"""


from PIL import Image, ImageTk
import os
import shutil
import tkinter as tk
import tkinter.messagebox


PADDING = 10


class CategorySorter:
    """
    A GUI application for sorting images into categories.
    """

    def __init__(self, root, imageFiles, config):
        """
        Initializes the application.

        Args:
            root (tk.Tk): The root tkinter window.
            imageFiles (list): A list of paths to the images to be sorted.
            config (dict): The configuration loaded from config.json.
        """
        self.root = root
        self.imageFiles = imageFiles
        self.config = config
        self.categories = config.get('categories', [])
        self.currentImageIndex = 0

        self.root.title("czimagesort - categorise")
        self.windowWidth = int(self.root.winfo_screenwidth() / 2)
        self.windowHeight = self.root.winfo_screenheight()
        self.root.geometry(f"{self.windowWidth}x{self.windowHeight}+{self.windowWidth}+0")

        mainFrame = tk.Frame(root, padx=PADDING, pady=PADDING)
        mainFrame.pack(fill=tk.BOTH, expand=True)

        self.imageFrame = tk.Frame(mainFrame)
        self.imageFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.buttonFrame = tk.Frame(mainFrame, padx=PADDING)
        self.buttonFrame.pack(side=tk.RIGHT, fill=tk.Y)

        self.imageLabel = tk.Label(self.imageFrame, text="Loading images...")
        self.imageLabel.pack(fill=tk.BOTH, expand=True)

        self.createButtons()

        self.root.bind('<Key>', self.keyPressed)

        self.showNextImage()
    #__init__


    def createButtons(self):
        """
        Creates the category and control buttons based on the config.
        """
        for category in self.categories:
            label = category.get('label', 'No Label')
            directory = category.get('directory')
            shortcut = category.get('shortcut')

            if not directory:
                continue
            #if

            os.makedirs(directory, exist_ok=True)

            btn = tk.Button(
                self.buttonFrame,
                text=f"{shortcut}: {label}",
                command=lambda dest=directory: self.moveImageAndAdvance(dest)
            )
            btn.pack(pady=PADDING, fill=tk.X)

        separator = tk.Frame(self.buttonFrame, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=PADDING, pady=PADDING)

        self.skipShortcut = self.config.get('skip_shortcut', 'space')
        skipButton = tk.Button(
            self.buttonFrame,
            text=f"{self.skipShortcut}: skip",
            command=self.showNextImage
        )
        skipButton.pack(pady=5, fill=tk.X)
    #createButtons


    def moveImageAndAdvance(self, destDir):
        """
        Moves the current image to the specified directory and shows the next one.
        """
        if self.currentImageIndex >= len(self.imageFiles):
            return
        #if

        sourcePath = self.imageFiles[self.currentImageIndex]

        if not os.path.exists(sourcePath):
            print(f"Warning: Source file not found, skipping: {sourcePath}")
            self.showNextImage()
            return
        #if

        filename = os.path.basename(sourcePath)
        destPath = os.path.join(destDir, filename)

        try:
            print(f"'{sourcePath}' --> '{destPath}'")
            shutil.move(sourcePath, destPath)
        except Exception as e:
            print(f"Error moving file: {e}")
            tk.messagebox.showerror("File Error", f"Could not move file: {e}")
            return
        #except

        self.showNextImage()
    #moveImageAndAdvance


    def showNextImage(self):
        """
        Displays the next image in the list.
        """
        if self.currentImageIndex >= len(self.imageFiles):
            self.root.quit()
            return
        #if

        filepath = self.imageFiles[self.currentImageIndex]

        try:
            img = Image.open(filepath)
            img.thumbnail((int(self.windowWidth * 0.7), int(self.windowHeight * 0.9)),
                          Image.Resampling.LANCZOS)
            self.tkImg = ImageTk.PhotoImage(img)
            self.imageLabel.config(image=self.tkImg)
            self.root.title(f"Image Sorter - "
                            f"{os.path.basename(filepath)} ({self.currentImageIndex + 1}"
                            f"/{len(self.imageFiles)})")
        except Exception as e:
            print(f"Error loading image {filepath}: {e}")
            # If an image fails to load, we skip it automatically
            self.showNextImage()
        #except

        self.currentImageIndex += 1

        if self.currentImageIndex >= len(self.imageFiles):
            self.root.quit()
            return
        #if

    #showNextImage


    def keyPressed(self, event):
        """
        Handles keyboard shortcuts.
        """
        pressedKey = event.keysym.lower()

        if pressedKey == self.skipShortcut:
            self.showNextImage()
            return
        #if

        for category in self.categories:
            if pressedKey == category.get('shortcut', '').lower():
                self.moveImageAndAdvance(category['directory'])
                return
            #if
        #for
    #key_pressed

#class CategorySorter


### aczutro ###################################################################
