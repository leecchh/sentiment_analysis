# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""

      self.dictP1 = {}
      self.dictN1 = {}
      if(os.path.isfile("dictP1.txt")):
         self.dictP1=self.load("dictP1.txt")
         self.dictN1=self.load("dictN1.txt")
      else:
         self.train()
      print len(self.dictN1)
      print len(self.dictP1)

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      lFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      lFileListP = []
      lFileListN = []
      posString='movies-5'
      negString='movies-1'

      for string in lFileList:
         if(string.startswith(posString)):
            lFileListP.append(string)
         else:
            lFileListN.append(string)

      for Pfile in lFileListP:
         string="movies_reviews/"+Pfile
         revString=self.loadFile(string)
         lst=self.tokenize(revString)
         for word in lst:
            if self.dictP1.has_key(word):
               self.dictP1[word] = self.dictP1[word]+1
            else:
               self.dictP1[word] = 1

      for Nfile in lFileListN:
         string="movies_reviews/"+Nfile
         revString=self.loadFile(string)
         lst=self.tokenize(revString)
         for word in lst:
            if self.dictN1.has_key(word):
               self.dictN1[word] = self.dictN1[word]+1
            else:
               self.dictN1[word] = 1

      self.save(self.dictP1,"dictP1.txt")
      self.save(self.dictN1,"dictN1.txt")

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

      PNum=0
      NNum=0

      for string in lFileList:
         if(string.startswith(posString)):
            PNum=PNum+1
         else:
            NNum=NNum+1

      # PriorPos=PNum*1.0/(PNum+NNum)
      # PriorNeg=1-PriorPos
      PriorPos=1
      PriorNeg=1
      probabilityP=math.log(PriorPos)
      totalFreqP=0
      for value in (self.dictP1).values():
         totalFreqP=totalFreqP+value

      probabilityN=math.log(PriorNeg)
      totalFreqN=0
      for value in (self.dictN1).values():
         totalFreqN=totalFreqN+value

      lst=self.tokenize(sText)
      for word in lst:
         wordFreq=0
         if (self.dictP1).has_key(word):
            wordFreq=(self.dictP1).get(word)
         else:
            wordFreq=1
         wordprob=wordFreq*1.0/(totalFreqP)
         probabilityP=probabilityP+math.log(wordprob*1.0)

      for word in lst:
         wordFreq=0
         if (self.dictN1).has_key(word):
            wordFreq=(self.dictN1).get(word)
         else:
            wordFreq=1
         wordprob=wordFreq*1.0/(totalFreqN)
         probabilityN=probabilityN+math.log(wordprob*1.0)

      probabilityP=abs(probabilityP)
      probabilityN=abs(probabilityN)

      print probabilityP
      print probabilityN

      if probabilityP>probabilityN:
         if (probabilityN>probabilityP-0.8):
            return "neutral"
         else:
            return "negative"
      if probabilityP<=probabilityN:
         if (probabilityP>probabilityN-0.8):
            return "neutral"
         else:
            return "positive"



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