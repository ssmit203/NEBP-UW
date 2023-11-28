# -*- coding: utf-8 -*-
"""
Created on Fri May 28 14:09:51 2021

This program contains the functions to:
    -get the file directory from the user using a Tkinter windows interface 
    -read in and clean profiles from GRAW generated text files
    -query user for save status and location

Last Updated: 10/9/2021 - 14:36PST
@author: Chambers,Alex
"""
import re
import os
import sys
import numpy as np
import pandas as pd
from io import StringIO
from tkinter import filedialog,Tk
from numpy.core.defchararray import lower
from datetime import datetime

def getUserInputFile(prompt):
    print(prompt)
    main = Tk()
    userInput = filedialog.askdirectory()
    main.destroy()
    if userInput == "":
        sys.exit()
    return userInput

def getUserInputTF(prompt):
    print(prompt+" (Y/N)")
    userInput = ""
    while not userInput:
        userInput = input()
        if lower(userInput) != "y" and lower(userInput) != "n":
            userInput = "please enter a 'Y' or 'N'"
        if lower(userInput) == "y":
            return True
        else:
             return

def readProfile(path,file):
        def atoi(text):
            return int(text) if text.isdigit() else text
        def natural_keys(text):
            return [atoi(c) for c in re.split(r'(\d+)', text)]
        if file.endswith(".txt"):
            # Used to fix a file reading error
            saveName = (file.split(".", 2))[0]
            contents = ""

            f = open(os.path.join(path, file), 'r')
            print("Running file "+saveName)
            #for line in f:
            #    isProfile = True
            contents = f.read()  
            #    print(line)                 
            f.close()
            
            contents = contents.split("\n")
            contents.pop(1)  # Remove units from temp file
            contents = "\n".join(contents)  # Reassemble string

            # Read in the data
            data = pd.read_csv(StringIO(contents),
                                  delim_whitespace=True, na_values=['-'])
                  
            return data, saveName       