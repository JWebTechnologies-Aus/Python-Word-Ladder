import re

#This function does the same job as the regular input() function, however it also checks for actual input length and for the presence of letters or numbers (if specified). If the input does not match the requirements, the prompt is looped until it does.
def inputCheck(prompt="",check=True):
    text = None
    while True:
        text = input(prompt)
        if len(text) == 0:
            print("Error, no input given\n")
            continue
        if not text.isalpha() and check:
            print("Error, cannot include numbers or punctuation.\n")
            continue
        break
    return text

#This function gets input for a file name/path, iterates through all the lines in the file and appends them to a list. The list is then returned. All relevant error handling is done within this function.
def getListFromFile():
  try:
    file = open(inputCheck("Enter dictionary name: ", check=False))
  except:
    print("Error, dictionary file does not exist.")
    exit(0)
  lines = file.readlines()
  for line in range(len(lines)):  # This strips the lines and removes any empty lines from the list
    lines[line] = lines[line].strip()
    if lines[line] == "":
      lines.pop(line)
  if len(lines) == 0:  # Closes the program if the file is empty.
    print("Error, file is empty.")
    exit(0)
  return lines

#TThis function takes two lists. It iterates over each item of the first list and if that item occurs in the second list, it is removed from the second list.
def removeBlacklistedWords(blacklist, lines):
  for word in blacklist:
    if word in lines:
      lines.remove(word)
  return lines


#This function takes two strings. It generates a list of all the individual characters that occur in the same position in each string. It then returns the length of that list. Thus it compares the similarity between the current step in the word ladder and the final target.
def same(item, target):
  return len([c for (c, t) in zip(item, target) if c == t])


#This function generates a list of words from the dictionary matching a pattern given to it in the form of a string. A ‘.’ character is used to denote a wild card (meaning it can be any character).
def build(pattern, words, seen, list):
  return [word for word in words
                 if re.search(pattern, word) and word not in seen.keys() and
                    word not in list]

def find(word, words, seen, target, path):
  list = []
  fixedIndexes=[]
  if same(word,target) > 0:
    for i in range(len(target)): # This loop is responsible for fixing letters in place if they match the target word
      if path[-1][i] == target[i]:
        fixedIndexes.append(i)
  for i in range(len(word)):
    if i not in fixedIndexes:
      list += build(word[:i] + "." + word[i + 1:], words, seen, list)
  if len(list) == 0:
    return False
  list = sorted([(same(w, target), w) for w in list], reverse=True)
  for (match, item) in list:
    #Match shows how many letters are in the current word (item) that are shared with the final word. It is appended if it is the equivalent of all letters - 1
    if match >= len(target) - 1:
      if match == len(target) - 1:
        path.append(item)
      return True
    seen[item] = True
  for (match, item) in list:
    path.append(item)
    if find(item, words, seen, target, path):
      return True
    path.pop()


#Open and read file. All words are on a separate line, ie. each line is a single word. Hence the variable 'lines' will contain a list of single words ending in '\n'.
lines = getListFromFile()

#Option to provide a blacklist file
blacklist = ""
while blacklist != "y" and blacklist != "n":
  blacklist = input("Would you like to provide a blacklist dictionary (Y/N)? ").lower()
  if blacklist != "y" and blacklist != "n":
    print("Error, please select 'y' or 'n' (case-insensitive)\n")
    continue
  if blacklist == "y":
    blacklistLines = getListFromFile()
    lines = removeBlacklistedWords(blacklistLines, lines)


#Gets input for the start word. Creates a list of words from the values of 'lines' that have a length the same as the length of the start word (after they have been stripped of '\n'). Also obtains input from the target word.
while True:
  words = []
  start=""
  while start not in words: #Loop to ensure start word is in the dictionary.
    start = inputCheck("Enter start word:").lower() #Must be lowercase in order to compare later.
    for line in lines:
      word = line.rstrip()
      if len(word) == len(start):
        words.append(word)
    if start not in words:
      print("Error, that word is not in my dictionary.\n")
      words=[]
  target=""
  #Input function has been put in a while loop to handle the potential length mismatch error and ensure that the target word is in the dictionary.
  while len(target) != len(start) or target not in words:
    target = inputCheck("Enter target word:").lower()
    if len(target) != len(start):
      print("Error, the target word must be the same length as the start word (", len(start), "letters ).\n")
    elif target not in words:
      print("Error, that word is not in my dictionary.\n")
    break
  break

allpaths = ""
while allpaths != "all" and allpaths != "single":
  allpaths = input("Would you like to generate a set of all possible unique paths or the shortest single path (type 'all' or 'single') ? ").lower()
  if allpaths != "all" and allpaths != "single":
    print("Error, please select 'all' or 'single' (case-insensitive)\n")
    continue
  allpaths = allpaths == "all"
  break

count = 0
path = [start]
seen = {start : True}

while True:
  path=[start]
  seen = {start : True}
  pathfound = find(start, words, seen, target, path)
  if pathfound:
    path.append(target)
    print(len(path) - 1, path)
  elif not pathfound and not allpaths:
    print("No Paths Found")
    break
  elif (not pathfound and allpaths):
    print("No more paths")
    break
  if not allpaths:
    break
  for word in path:
    if word in words and word != start and word != target:
      words.remove(word)
    if len(path) - 1 <= 1:
      words.remove(word)
  if len(path) - 1 <= 1:
    print("This is a special case. The target can be achieved in one step. Below are all technically paths")
else:
  print("No path found")

