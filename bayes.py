# File: bayes.py
# Members and netids:
# Chung Ho Lee, chl433
# Edward Hu, ehe839
# Atul Adhikari, aca089

# Date: 5/23/2016
# Group work statement: All group members were present and contributing during all work on this project

import math, os, pickle, re

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""

      self.dictP = {}
      self.dictN = {}
      if(os.path.isfile("dictP.txt")):
         self.dictP=self.load("dictP.txt")
         self.dictN=self.load("dictN.txt")
      else:
         self.train()

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      lFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      lFileListP = []
      lFileListN = []
      posString='movies-5' #What positive movies start with
      negString='movies-1' #What negative movies start with

      # Append the strings of file names in
      # Different lists depending on type
      for string in lFileList:
         if(string.startswith(posString)):
            lFileListP.append(string)
         else:
            lFileListN.append(string)

      # Store every word in positive files in dictionary
      for Pfile in lFileListP:
         string="movies_reviews/"+Pfile
         revString=self.loadFile(string)
         lst=self.tokenize(revString)
         for word in lst:
            if self.dictP.has_key(word):
               self.dictP[word] = self.dictP[word]+1
            else:
               self.dictP[word] = 1

      # Store every word in negative files in dictionary
      for Nfile in lFileListN:
         string="movies_reviews/"+Nfile
         revString=self.loadFile(string)
         lst=self.tokenize(revString)
         for word in lst:
            if self.dictN.has_key(word):
               self.dictN[word] = self.dictN[word]+1
            else:
               self.dictN[word] = 1

      #Save the dictionaries in 2 files
      self.save(self.dictP,"dictP.txt")
      self.save(self.dictN,"dictN.txt")

   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      lFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      lFileListP = []
      lFileListN = []
      posString='movies-5'
      negString='movies-1'

      PNum=0 #Initialize values
      NNum=0 #Initialize values

      # Calculate number of positive and negative files
      for string in lFileList:
         if(string.startswith(posString)):
            PNum=PNum+1
         else:
            NNum=NNum+1

      PriorPos=PNum*1.0/(PNum+NNum)
      PriorNeg=1-PriorPos

      # Initialize probability
      probabilityP=1
      probabilityN=1

      # Find frequency of positive words
      totalFreqP=0
      for value in (self.dictP).values():
         totalFreqP=totalFreqP+value
      
      # Find frequency of negative words
      totalFreqN=0
      for value in (self.dictN).values():
         totalFreqN=totalFreqN+value

      # Compute probabilityP for each file
      lst=self.tokenize(sText)
      for word in lst:
         wordFreq=0
         if (self.dictP).has_key(word):
            wordFreq=(self.dictP).get(word)
         else:
            wordFreq=1
         wordprob=wordFreq*1.0/(totalFreqP)
         probabilityP=probabilityP+math.log(wordprob*1.0)

      # Compute probabilityN for each file
      for word in lst:
         wordFreq=0
         if (self.dictN).has_key(word):
            wordFreq=(self.dictN).get(word)
         else:
            wordFreq=1 #Default frequency 1 if not found
         wordprob=wordFreq*1.0/(totalFreqN)
         probabilityN=probabilityN+math.log(wordprob*1.0)

      # Take absolute value of computed log probability
      probabilityP=abs(probabilityP)
      probabilityN=abs(probabilityN)

      if probabilityP>probabilityN:
         if (probabilityN>probabilityP-0.8):
            return "neutral" #Values are too close, return neutral
         else:
            return "negative" #More likely to be negative, return
      if probabilityP<=probabilityN:
         if (probabilityP>probabilityN-0.8):
            return "neutral" #Values are too close, return neutral
         else:
            return "positive" #More likely to be positive, return

   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens