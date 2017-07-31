import re

#This function does the same job as the regular input() function, however it also checks for actual input length and for the presence of letters or numbers (if specified)
def inputCheck(prompt="",check=True):
    text = None
    while True:
        text = input(prompt)
        if len(text) == 0:
            print("Error, no input given\n")
            continue
        if not text.isalpha() and check:
            print("Error, cannot include numbers or punctuation\n")
            continue
        break
    return text

#This function removes all words from the blacklist file from the word list (if they appear in it)
def removeBlacklistedWords(blacklist, lines):
  for word in blacklist:
    if word in lines:
      lines.remove(word)
  return lines


#This function generates a list of all characters appearing in the string given to it and the end string specified by the user. It returns the length of this list (ie. the number of values that are the same in each list)
def same(item, target):
  return len([c for (c, t) in zip(item, target) if c == t])


#Generates a list of words from the dictionary where every letter matches except ".". This character is a wildcard added into a word by the loop that this is called from in thee find function.
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
try:
  file = open(inputCheck("Enter dictionary name: ",check=False))
except:
  print("Error, dictionary file does not exist.")
  exit(0)
lines = file.readlines()
for line in range(len(lines)): #This strips the lines and removes any empty lines from the list
  lines[line]=lines[line].strip()
  if lines[line] == "":
    lines.pop(line)
if len(lines) ==0: #Closes the program if the file is empty.
  print("Error, file is empty.")
  exit(0)

#Option to provide a blacklist file
blacklist = ""
while blacklist != "y" and blacklist != "n":
  blacklist = input("Would you like to provide a blacklist dictionary (Y/N)? ").lower()
  if blacklist != "y" and blacklist != "n":
    print("Error, please select 'y' or 'n' (case-insensitive)\n")
    continue
  if blacklist == "y":
    try:
      wordstoRemove = open(inputCheck("Enter blacklist filename: ",check=False)).readlines()
    except:
      print("Error, blacklist file does not exist.")
      exit()
    for line in range(len(wordstoRemove)):  # This strips the lines and removes any empty lines from the list
      wordstoRemove[line] = wordstoRemove[line].strip()
      if wordstoRemove[line] == "":
        wordstoRemove.pop(line)
    if len(wordstoRemove) == 0:  # Closes the program if the file is empty.
      print("Error, file is empty.")
      exit(0)
    lines = removeBlacklistedWords(wordstoRemove, lines)


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

count = 0
path = [start]
seen = {start : True}
if find(start, words, seen, target, path):
  path.append(target)
  print(len(path) - 1, path)
else:
  print("No path found")

