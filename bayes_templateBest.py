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
            if self.dictP.has_key(word):
               self.dictP[word] = self.dictP[word]+1
            else:
               self.dictP[word] = 1

      for Nfile in lFileListN:
         string="movies_reviews/"+Nfile
         revString=self.loadFile(string)
         lst=self.tokenize(revString)
         for word in lst:
            if self.dictN.has_key(word):
               self.dictN[word] = self.dictN[word]+1
            else:
               self.dictN[word] = 1

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

      PNum=0
      NNum=0

      for string in lFileList:
         if(string.startswith(posString)):
            PNum=PNum+1
         else:
            NNum=NNum+1

      PriorPos=PNum*1.0/(PNum+NNum)
      PriorNeg=1-PriorPos
      probabilityP=math.log(PriorPos)
      totalFreqP=0
      for value in (self.dictP).values():
         totalFreqP=totalFreqP+value

      probabilityN=math.log(PriorNeg)
      totalFreqN=0
      for value in (self.dictN).values():
         totalFreqN=totalFreqN+value

      lst=self.tokenize(sText)
      for word in lst:
         wordFreq=0
         if (self.dictP).has_key(word):
            wordFreq=(self.dictP).get(word)
         else:
            wordFreq=1
         wordprob=wordFreq*1.0/(totalFreqP)
         probabilityP=probabilityP+math.log(wordprob*1.0)

      for word in lst:
         wordFreq=0
         if (self.dictN).has_key(word):
            wordFreq=(self.dictN).get(word)
         else:
            wordFreq=1
         wordprob=wordFreq*1.0/(totalFreqN)
         probabilityN=probabilityN+math.log(wordprob*1.0)

      probabilityP=abs(probabilityP)
      probabilityN=abs(probabilityN)

      stringLen=len(lst) # Get the number of strings in the input
      lensqt=math.sqrt(stringLen) # Takes the square root of the number of strings
      print probabilityP
      print probabilityN

      if probabilityP>probabilityN:
         if (probabilityN>probabilityP-0.7*lensqt):
            return "neutral"
         else:
            return "negative"
      if probabilityP<=probabilityN:
         if (probabilityP>probabilityN-0.7*lensqt):
            return "neutral"
         else:
            return "positive"

   def crossVal(self):
      lFileList = [] #The whole list
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      lFileListP = [] #Positive in the list
      lFileListN = [] #Negative in the list
      posString='movies-5'
      negString='movies-1'

      for string in lFileList:
         if(string.startswith(posString)):
            lFileListP.append(string)
         else:
            lFileListN.append(string)
      
      Plength=len(lFileListP)
      Nlength=len(lFileListN)
      Psubset=Plength/10
      Nsubset=Nlength/10
      empty=[]
      lFileListSubsetP=[]
      lFileListSubsetN=[]
      for num in range(0,10):
         lFileListSubsetP.append(empty)
         lFileListSubsetN.append(empty)

      for num in range(0,10):
         jump1=num*Psubset
         jump2=num*Nsubset
         for x in range(0+jump1,Psubset+jump1):
            lFileListSubsetP[num].append(lFileListP[x])
         for x in range(0+jump2,Nsubset+jump2):
            lFileListSubsetN[num].append(lFileListN[x])

      dictArrayP=[]
      for num in range(0,10):
         dictArrayP.append({})

      dictArrayN=[]
      for num in range(0,10):
         dictArrayN.append({})

      for numsubset in range(0,10):
         for num in range(0,10):
            if (numsubset!=num):
               for Pfile in lFileListSubsetP[num]:
                  string="movies_reviews/"+Pfile
                  revString=self.loadFile(string)
                  lst=self.tokenize(revString)
                  for word in lst:
                     if dictArrayP[numsubset].has_key(word):
                        (dictArrayP[numsubset])[word] = (dictArrayP[numsubset])[word]+1
                     else:
                        (dictArrayP[numsubset])[word] = 1

      for numsubset in range(0,10):
         for num in range(0,10):
            if (numsubset!=num):
               for Nfile in lFileListSubsetN[num]:
                  string="movies_reviews/"+Nfile
                  revString=self.loadFile(string)
                  lst=self.tokenize(revString)
                  for word in lst:
                     if dictArrayN[numsubset].has_key(word):
                        (dictArrayN[numsubset])[word] = (dictArrayN[numsubset])[word]+1
                     else:
                        (dictArrayN[numsubset])[word] = 1

      recallP=[]
      recallN=[]
      precisionP=[]
      precisionN=[]
      numerator=0
      denominator=0

      for numsubset in range(0,10):
         numerator=0
         denominator=0
         for Pfile in LFileListSubsetP[num]:
            value=self.classifyTest(Pfile,dictArrayP[numsubset],dictArrayN[numsubset])
            if (value is "positive"):
               numerator+=1
               denominator+=1
            else:
               denominator+=1
         recallP.append(numerator*1.0/denominator)

      for numsubset in range(0,10):
         numerator=0
         denominator=0
         for Nfile in LFileListSubsetN[num]:
            value=self.classifyTest(Nfile,dictArrayP[numsubset],dictArrayN[numsubset])
            if (value is "negative"):
               numerator+=1
               denominator+=1
            else:
               denominator+=1
         recallN.append(numerator*1.0/denominator)

      print recallP
      print recallN

   def classifyTest(self, sText, dictP,dictN):
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

      PriorPos=PNum*1.0/(PNum+NNum)
      PriorNeg=1-PriorPos
      probabilityP=math.log(PriorPos)
      totalFreqP=0
      for value in (dictP).values():
         totalFreqP=totalFreqP+value

      probabilityN=math.log(PriorNeg)
      totalFreqN=0
      for value in (dictN).values():
         totalFreqN=totalFreqN+value

      lst=self.tokenize(sText)
      for word in lst:
         wordFreq=0
         if (dictP).has_key(word):
            wordFreq=(dictP).get(word)
         else:
            wordFreq=1
         wordprob=wordFreq*1.0/(totalFreqP)
         probabilityP=probabilityP+math.log(wordprob*1.0)

      for word in lst:
         wordFreq=0
         if (dictN).has_key(word):
            wordFreq=(dictN).get(word)
         else:
            wordFreq=1
         wordprob=wordFreq*1.0/(totalFreqN)
         probabilityN=probabilityN+math.log(wordprob*1.0)

      probabilityP=abs(probabilityP)
      probabilityN=abs(probabilityN)

      stringLen=len(lst) # Get the number of strings in the input
      lensqt=math.sqrt(stringLen) # Takes the square root of the number of strings
      print probabilityP
      print probabilityN

      if probabilityP>probabilityN:
         if (probabilityN>probabilityP-0.7*lensqt):
            return "neutral"
         else:
            return "negative"
      if probabilityP<=probabilityN:
         if (probabilityP>probabilityN-0.7*lensqt):
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