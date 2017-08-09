import unittest
import re
#To generate a list of words from the game dictionary for testing, as all testing words will have 4 letters, only these are imported.
gameWords=[]
for line in open("dictionary.txt"):
    line = line.strip()
    if len(line) == 4:
        gameWords.append(line)


#This function does the same job as the regular input() function, however it also checks for actual input length and for the presence of letters or numbers (if specified). If the input does not match the requirements, the prompt is looped until it does.
def inputCheck(string,check=True):
    text = None
    while True:
        text = string
        if len(text) == 0:
            return ("Error, no input given\n")
        if not text.isalpha() and check:
            return ("Error, cannot include numbers or punctuation.\n")
        break
    return text

#This function gets input for a file name/path, iterates through all the lines in the file and appends them to a list. The list is then returned. All relevant error handling is done within this function.
def getListFromFile(filename):
  try:
    file = open(filename)
  except:
    print("Error, dictionary file does not exist.")
    exit(0)
  lines = file.readlines()
  for line in range(len(lines)):  # This strips the lines and removes any empty lines from the list
    lines[line] = lines[line].strip()
    if lines[line] == "":
      lines.pop(line)
  file.close()
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
      return path
    path.pop()

class TestFileNameInputAndHandling(unittest.TestCase):
    def test_invalidFile(self):
        self.assertRaises((SystemExit, FileNotFoundError),getListFromFile,'bad')
    def test_emptyFile(self):
        self.assertRaises(SystemExit,getListFromFile,'blank.txt')

class TestCheckWordInput(unittest.TestCase):
    def test_punctuation(self):
        self.assertEqual(inputCheck('word.'), "Error, cannot include numbers or punctuation.\n")

    def test_numbers(self):
        self.assertEqual(inputCheck('word4'), "Error, cannot include numbers or punctuation.\n")

class TestBlacklisting(unittest.TestCase):
    def test_successfulWithFullLists(self):
        self.assertEqual(removeBlacklistedWords(['test', 'function'],['test', 'function', 'assert', 'true']), ['assert','true'])

    def test_successfulWithAdditionalWords(self):
        self.assertEqual(removeBlacklistedWords(['test', 'function', 'bananas', 'apple'], ['test', 'function', 'assert', 'true']),
                         ['assert', 'true'])

class TestWordComparator(unittest.TestCase):
    def test_twoStrings1(self):
        self.assertEqual(same('list','seek'), 0)
    def test_twoStrings2(self):
        self.assertEqual(same('lead','gold'), 1)
    def test_twoStrings3(self):
        self.assertEqual(same('letter','letter'), 6)

class TestMatchingWordsListBuilder(unittest.TestCase):
    def test_patterningWorks(self):
        self.assertEqual(build('test', ['test','assert','best'],{},[]),['test'])
    def test_wildcardWorks(self):
        self.assertEqual(build('.est', ['test','assert','best'],{},[]),['test','best'])
    def test_seenBlacklistWorks(self):
        self.assertEqual(build('.est', ['test','assert','best'],{'test': True},[]),['best'])
    def test_listBlacklistWorks(self):
        self.assertEqual(build('.est', ['test','assert','best'],{},['test']),['best'])

class TestFindingPaths(unittest.TestCase):
    def test_correctPathFound1(self):
        self.assertEqual((find('lead', gameWords, {'lead':True},'gold', ['lead'])), ['lead', 'load', 'goad'])
    def test_correctPathFound2(self):
        self.assertEqual((find('hide', gameWords, {'hide':True},'seek', ['hide'])), ['hide', 'side', 'site', 'sits', 'sies', 'sees'])

if __name__ == '__main__':
    unittest.main()
