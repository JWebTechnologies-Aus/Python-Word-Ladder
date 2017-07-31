import re

#This function generates a list of all characters appearing in the string given to it and the end string specified by the user. It returns the length of this list (ie. the number of values that are the same in each list)
def same(item, target):
  #print([c for (c, t) in zip(item, target) if c == t])
  return len([c for (c, t) in zip(item, target) if c == t])


#Generates a list of words from the dictionary where every letter matches except ".". This character is a wildcard added into a word by the loop that this is called from in thee find function.
def build(pattern, words, seen, list):
  return [word for word in words
                 if re.search(pattern, word) and word not in seen.keys() and
                    word not in list]

def find(word, words, seen, target, path):
  list = []
  fixedIndexes=[] #ADD STARTS HERE
  if same(word,target) > 0:
    for i in range(len(target)):
      if path[-1][i] == target[i]:
        fixedIndexes.append(i) #ADD ENDS HERE
  for i in range(len(word)):
    if i not in fixedIndexes:
      list += build(word[:i] + "." + word[i + 1:], words, seen, list)
    # for word in list:
    #   if same(word,target) == len(target)-1:
    #     seen[word] = True
    #     path.append(word)
    #     return True
  if len(list) == 0:
    return False
  list = sorted([(same(w, target), w) for w in list], reverse=True) #CHANGED
  #print(path[-1])
  #print(list)
  for (match, item) in list:
    #Match shows how many letters are in the current word (item) that are shared with the final word. It is appended if it is the equivalent of all letters - 1
    if match >= len(target) - 1:
      if match == len(target) - 1:
        path.append(item)
      return True
    seen[item] = True
  #This loop repeats the find function until a match is found?
  for (match, item) in list:
    path.append(item)
    if find(item, words, seen, target, path):
      return True
    path.pop()


#Open and read file. All words are on a separate line, ie. each line is a single word. Hence the variable 'lines' will contain a list of single words ending in '\n'.
fname = input("Enter dictionary name: ")
file = open(fname)
lines = file.readlines()

#Gets input for the start word. Creates a list of words from the values of 'lines' that have a length the same as the length of the start word (after they have been stripped of '\n'). Also obtains input from the target word.
while True:
  start = input("Enter start word:")
  words = []
  for line in lines:
    word = line.rstrip()
    if len(word) == len(start):
      words.append(word)
  target = input("Enter target word:")
  break

count = 0
path = [start]
seen = {start : True}
if find(start, words, seen, target, path):
  path.append(target)
  print(len(path) - 1, path)
else:
  print("No path found")

