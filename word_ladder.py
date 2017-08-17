''''
Word Ladder Generation Tool. 
(word_ladder.py)
 
Modified by: Jake Jones, Ashman Malik
Author: Unknown
 
The goal of this project was to repair an undocumented python program (word_ladder.py) that was used to generate a word ladder based on words in a provided dictionary file (such that each word produced differs from the previous one on the ladder by one letter, connecting a specified start word to a finish word. The original author of this code is unknown.
 
Details and descriptions of code can be found in the accompanying documentation file (word_ladder_documentation.doc).
'''

import re

def inputCheck(prompt="",check=True):
    text = None
    while True:
        text = input(prompt) #Get input from user.
        if len(text) == 0: #Check that the input given was not an empty string.
            print("Error, no input given\n")
            continue
        if not text.isalpha() and check: #Check that the line has no numbers or punctuation (if this option is selected via the parameters - True by default)
            print("Error, cannot include numbers or punctuation.\n")
            continue
        break
    return text

def getListFromFile():
  try:
    file = open(inputCheck("Enter dictionary name: ", check=False)) #Get input for file name.
  except: #File is not found - this is checked to be raised in unittesting.
    print("Error, dictionary file does not exist.")
    exit(0)
  lines = file.readlines() #Returns a list of all the lines in the file.
  for line in range(len(lines)):
    lines[line] = lines[line].strip() #Remove any white space or special characters from the line ends.
    if lines[line] == "":
      lines.pop(line) #Remove the line if it is empty.
  if len(lines) == 0:
    print("Error, file is empty.")
    exit(0) #Closes the program if the file is empty.
  return lines

def same(item, target):
  return len([itemLetter for (itemLetter, targetLetter) in zip(item, target) if itemLetter == targetLetter]) #Takes two strings, generates a list of all the individual characters that occur in the same position in each string and returns the length of that list (ie. how similar the word is to the final target.

def build(pattern, words, seen, potentialNextWords):
  return [word for word in words if re.search(pattern, word) and word not in seen.keys() and word not in potentialNextWords] #Generates a list of words from the dictionary matching a pattern given to it in the form of a string. A ‘.’ character is used to denote a wild card (meaning it can be any character).

def find(word, words, seen, target, path):
  potentialNextWords = []
  fixedIndexes=[i for i in range(len(word)) if word[i] == target[i]] #Generates a list of indexes in which there is a matching letter for both the current word and the target word.
  for i in [index for index in range(len(word)) if index not in fixedIndexes]: #Iterating through a list of indexes of the current word that are NOT IN fixedIndexes.
    potentialNextWords += build(word[:i] + "." + word[i + 1:], words, seen, potentialNextWords) #Building a list of the potentialNextWords while ignoring the indexes that in fixedIndexes.
  if len(potentialNextWords) == 0: #End the function (and all its recursions) with a negative return statement if there are no more potential next words
    return False
  potentialNextWords = sorted([(same(word, target), word) for word in potentialNextWords], reverse=True) #Generate a list of tuples - containing the potenial next words and their similarity to the target word (match). Ordered with most similar words first.
  for (match, item) in potentialNextWords: #End the function (and all its recursions) with a positive return statement if the potentialNextWords list has a word that can be the final step before the target word OR the target word itself.
    if match >= len(target) - 1:
      if match == len(target) - 1:
        path.append(item) #If the potentialNextWords does NOT contain the target, but a word that can be the final one before the target, append the word to the path before stopping the function.
      return True
    seen[item] = True #If function is not ended, add each word in potentialNextWords to the seen dictionary.
  for (match, item) in potentialNextWords: #Iterate through the list of potentialNextWords, add each item to the path before recursively running find(). If a path is found, return True and print the path. If not, remove the word and try again with the next one.
    path.append(item)
    if find(item, words, seen, target, path):
      return True
    path.pop()

##############################
### Beginning of main code ###
##############################

masterDictionary = getListFromFile()
originalSeen = {}

#Get input for blacklisting functionality.
while True:
  blacklist = input("Would you like to provide a blacklist dictionary (Y/N)? ").lower() #Option to provide blacklist dictionary file.
  if blacklist != "y" and blacklist != "n":
    print("Error, please select 'y' or 'n' (case-insensitive)\n")
    continue
  if blacklist == "y":
    blacklistDictionary = getListFromFile()
    for word in blacklistDictionary:
      originalSeen[word] = True
  break

#Get input for start word
while True: #Loop to ensure start word is in the dictionary. Uses True, rather than condition so it does not need to evaluate a second time after printing error.
  start = inputCheck("Enter start word:").lower() 
  if start not in masterDictionary: #Check that start word is in the dictionary.
    print("Error, that word is not in my dictionary.\n")
    continue
  break
originalSeen[start] = True

#Get input for target word
while True:
  target = inputCheck("Enter target word:").lower()
  if start == target: #Checks that the start and target word are not the same (does this first because it is the quickest comparison).
    print("Error, please choose a different word. Target cannot be the same as start.\n")
    continue  
  elif len(target) != len(start): #Checks that the length of both words match.
    print("Error, the target word must be the same length as the start word (", len(start), "letters ).\n")
    continue
  elif target not in masterDictionary: #Checks that the target word is in the dictionary (does this last because it takes the longest to evaluate).
    print("Error, that word is not in my dictionary.\n")
    continue
  break

words = [word for word in masterDictionary if len(word) == len(start)] #Generates working dictionary (list of words in the dictionary that match the length of the start and target words).

#Get input for what the user wants to find (optimal path, ALL unique paths or single SHORTEST path).
shortestPath=False
while True:
  allpaths = input("Would you like to generate a single (OPTIMAL) path, a set of ALL possible unique paths or the SHORTEST path NOTE: the final two options will take longer (type 'optimal','all' or 'shortest') ? ").lower()
  if allpaths != "all" and allpaths != "optimal" and allpaths != "shortest": #Check that input is valid. Only two possible inputs accepted (case insensitive) - 'all' or 'single'.
    print("Error, please select 'optimal', 'single' or 'all' (case-insensitive)\n")
    continue
  if allpaths == "shortest":
    print("Beware: This process may take some time (in some cases) because I need to examine ALL unique posibilities. To find a the quickest single path, much faster, use the 'single' option for the OPTIMAL path. In some cases this may also be the shortest.") #Message to warn user that the process may take time to ensure the SHORTEST path is given. This time may vary.
    shortestPath = True
  allpaths = allpaths == "all"
  break

#Run the find() function to find all paths (or just the shortest).
if shortestPath: #Only initialize this variable when looking at the shortest path.
  minPath=None

while True:
  path = [start]
  seen = originalSeen.copy()
  pathfound = find(start, words, seen, target, path) #Obtain path, and get boolean depending on if the process is successful or not.
  if pathfound and not shortestPath: #Print the path and its length if it can be found.
    path.append(target)
    print(len(path) - 1, " >> ".join(path), "\n")
  elif shortestPath and pathfound: #If looking for shortest path, just append the paths to the paths array
    path.append(target)
    if pathfound and (minPath == None or len(path) -1 < len(minPath)): #Keep shortest path in memory and check it against the latest path. Replace if it is shorter.
      minPath= path
  elif not pathfound: #Print 'No path found' if only looking for single path and cannot find one or shortest path if desired.
    if allpaths:
      print("No more paths")
    elif shortestPath: #Print the shortest path when no more paths can be found.
      if minPath == None:
        print("No path found")
        break
      print(len(minPath) - 1, " >> ".join(minPath)) #Print the length of the shortest path and the path
    else:
      print("No path found")
    break
  if not allpaths and not shortestPath: #Break out of the loop (and end program) if only looking for a single path (the single OPTIMAL path).
    break
  if len(path) <= 2: #Warns that the path only has one step and terminates the program. NOTE: this will only be reached if the user is trying to find all paths.
    print("This is a special case. The target can be achieved in one step. Whilst there may technically be more paths, they will not be shown. \n")
    break
  for word in path: #Adds all words in the path into the dictionary (originalSeen) that the seen dictionary for each iteration is copied from - this is how it finds all UNIQUE paths.
    originalSeen[word] = True



