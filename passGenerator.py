#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis Martínez Moreno PID: 6366100
"""

# first we import the libraries
import random, string
# Given the parameters from the promt, it generates the password
# manages different errors that might happen while introducing wrong attribute values
def generatePassword(nWords, caps, numbers, symbols):
    #First we read the wordlist (only English words in lower case)
    with open("./corncob_lowercase.txt", "r") as file:
        allText = file.read()
        words = list(map(str, allText.split()))
        # We select randomly a fixed number of words (4 by default)
        passwordWordsList = random.choices(words, k = nWords)
        # We capitalize the first letter of a given number of words randomly
        if caps > 0:
            if caps > nWords:
                caps = nWords
            selectedNum = []
            while caps > 0:
                numSelected = -1
                while (numSelected in selectedNum) or (numSelected == -1):
                    numSelected = random.randint(0, nWords-1)
                passwordWordsList[numSelected] = passwordWordsList[numSelected].capitalize()
                selectedNum.append(numSelected)
                caps = caps-1
        password = "".join(passwordWordsList)
        
        #We introduce randomly a number of numbers
        while numbers > 0:
            randPosition = random.randint(0,len(password))
            randNumber = str(random.randint(0,9))
            password = password[:randPosition] + randNumber + password[randPosition:]
            numbers = numbers-1
        #We introduce randomly a number of symbols
        while symbols > 0:
            randPosition = random.randint(0,len(password))
            randSym = random.choice(string.punctuation)
            password = password[:randPosition] + randSym + password[randPosition:]
            symbols = symbols-1

        return password