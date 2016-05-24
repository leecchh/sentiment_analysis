# File: bayesbest.py
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

      stringLen=len(lst) # Get the number of strings in the input
      lensqt1=math.sqrt(stringLen)
      lensqt=math.sqrt(lensqt1) # Takes the 4th root of the number of strings

      if probabilityP>probabilityN:
         if (probabilityN>probabilityP-0.7*lensqt): #Use lensqt in our classification
            return "neutral" #Values are too close, return neutral
         else:
            return "negative" #More likely to be negative, return
      if probabilityP<=probabilityN:
         if (probabilityP>probabilityN-0.7*lensqt): #Use lensqt in our classification
            return "neutral" #Values are too close, return neutral
         else:
            return "positive" #More likely to be positive, return

   def crossVal(self):
      """Cross validating data"""
      lFileList = [] #The whole list
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      lFileListP = [] #Positive in the list
      lFileListN = [] #Negative in the list
      posString='movies-5'
      negString='movies-1'

      #Initialize lFileListP and lFileListN
      for string in lFileList:
         if(string.startswith(posString)):
            lFileListP.append(string)
         else:
            lFileListN.append(string)

      # Initialize the subset length for each of 10 subsets
      Plength=len(lFileListP)
      Nlength=len(lFileListN)
      Nsubset=Nlength/10
      Psubset=Nsubset
      lFileListSubsetP=[[],[],[],[],[],[],[],[],[],[]]
      lFileListSubsetN=[[],[],[],[],[],[],[],[],[],[]]

      # Add files into each subset
      for num in range(0,10):
         jump=num*Psubset
         for x in range(0+jump,Psubset+jump):
            lFileListSubsetP[num].append(lFileListP[x])

      for num in range(0,10):
         jump=num*Nsubset
         for x in range(0+jump,Nsubset+jump):
            lFileListSubsetN[num].append(lFileListN[x])

      #Initialize dictionaries
      dictArrayP=[{},{},{},{},{},{},{},{},{},{}]
      dictArrayN=[{},{},{},{},{},{},{},{},{},{}]

      # Load dictionaries if already created
      if(os.path.isfile("dictP0.txt")):
         dictArrayP[0]=self.load("dictP0.txt")
         dictArrayP[1]=self.load("dictP1.txt")
         dictArrayP[2]=self.load("dictP2.txt")
         dictArrayP[3]=self.load("dictP3.txt")
         dictArrayP[4]=self.load("dictP4.txt")
         dictArrayP[5]=self.load("dictP5.txt")
         dictArrayP[6]=self.load("dictP6.txt")
         dictArrayP[7]=self.load("dictP7.txt")
         dictArrayP[8]=self.load("dictP8.txt")
         dictArrayP[9]=self.load("dictP9.txt")

         dictArrayN[0]=self.load("dictN0.txt")
         dictArrayN[1]=self.load("dictN1.txt")
         dictArrayN[2]=self.load("dictN2.txt")
         dictArrayN[3]=self.load("dictN3.txt")
         dictArrayN[4]=self.load("dictN4.txt")
         dictArrayN[5]=self.load("dictN5.txt")
         dictArrayN[6]=self.load("dictN6.txt")
         dictArrayN[7]=self.load("dictN7.txt")
         dictArrayN[8]=self.load("dictN8.txt")
         dictArrayN[9]=self.load("dictN9.txt")

      #Form dictionaries if they are not already there
      #For each word in each subset a dictionary is formed
      #Positive dictionary
      else:
         for numsubset in range(0,10):
            for num in range(0,10):
               if (numsubset!=num): #Do not include when numsubset=num
                  for Pfile in lFileListSubsetP[num]:
                     string="movies_reviews/"+Pfile
                     revString=self.loadFile(string)
                     lst=self.tokenize(revString)
                     for word in lst:
                        if dictArrayP[numsubset].has_key(word):
                           (dictArrayP[numsubset])[word] = (dictArrayP[numsubset])[word]+1
                        else:
                           (dictArrayP[numsubset])[word] = 1

         #Negative dictionary
         for numsubset in range(0,10):
            for num in range(0,10):
               if (numsubset!=num):#Do not include when numsubset=num
                  for Nfile in lFileListSubsetN[num]:
                     string="movies_reviews/"+Nfile
                     revString=self.loadFile(string)
                     lst=self.tokenize(revString)
                     for word in lst:
                        if dictArrayN[numsubset].has_key(word):
                           (dictArrayN[numsubset])[word] = (dictArrayN[numsubset])[word]+1
                        else:
                           (dictArrayN[numsubset])[word] = 1

         #Save dictionaries
         self.save(dictArrayP[0],"dictP0.txt")
         self.save(dictArrayP[1],"dictP1.txt")
         self.save(dictArrayP[2],"dictP2.txt")
         self.save(dictArrayP[3],"dictP3.txt")
         self.save(dictArrayP[4],"dictP4.txt")
         self.save(dictArrayP[5],"dictP5.txt")
         self.save(dictArrayP[6],"dictP6.txt")
         self.save(dictArrayP[7],"dictP7.txt")
         self.save(dictArrayP[8],"dictP8.txt")
         self.save(dictArrayP[9],"dictP9.txt")

         self.save(dictArrayN[0],"dictN0.txt")
         self.save(dictArrayN[1],"dictN1.txt")
         self.save(dictArrayN[2],"dictN2.txt")
         self.save(dictArrayN[3],"dictN3.txt")
         self.save(dictArrayN[4],"dictN4.txt")
         self.save(dictArrayN[5],"dictN5.txt")
         self.save(dictArrayN[6],"dictN6.txt")
         self.save(dictArrayN[7],"dictN7.txt")
         self.save(dictArrayN[8],"dictN8.txt")
         self.save(dictArrayN[9],"dictN9.txt")

      #Code for recall calculations
      recallP=[]
      recallN=[]
      numerator=0
      denominator=0

      #Do calculations for each subset for positive
      for numsubset in range(0,10):
         numerator=0
         denominator=0
         for Pfile in lFileListSubsetP[numsubset]:
            string="movies_reviews/"+Pfile
            pText=self.loadFile(string)
            value=self.classifyTest(pText,dictArrayP[numsubset],dictArrayN[numsubset])
            if (value=="positive"): #The case where file is correctly classified as positive
               numerator+=1
               denominator+=1
            else: #The case where positive file is classified as non-positive
               denominator+=1
         recallP.append(numerator*1.0/denominator) #Append to list

      #Do calculations for each subset for negative
      for numsubset in range(0,10):
         numerator=0
         denominator=0
         for Nfile in lFileListSubsetN[numsubset]:
            string="movies_reviews/"+Nfile
            nText=self.loadFile(string)
            value=self.classifyTest(nText,dictArrayP[numsubset],dictArrayN[numsubset])
            if (value=="negative"): #The case where file is correctly classified as negative
               numerator+=1
               denominator+=1
            else: #The case where negative file is classified as non-negative
               denominator+=1
         recallN.append(numerator*1.0/denominator) #Append to list

      #Code for precision calculations
      precisionP=[]
      precisionN=[]
      numerator2=0
      denominator2=0

      #Do calculations for each subset
      for numsubset in range(0,10):
         numerator=0
         denominator=0
         numerator2=0
         denominator2=0
         for Pfile in lFileListSubsetP[numsubset]:
            string="movies_reviews/"+Pfile
            pText=self.loadFile(string)
            value=self.classifyTestOrg(pText,dictArrayP[numsubset],dictArrayN[numsubset])
            if (value=="positive"): #The case where file is correctly classified as positive
               numerator+=1
               denominator+=1
            if (value=="negative"):#The case where positive file is classified as negative
               denominator2+=1
         for Nfile in lFileListSubsetN[numsubset]:
            string="movies_reviews/"+Nfile
            nText=self.loadFile(string)
            value=self.classifyTestOrg(nText,dictArrayP[numsubset],dictArrayN[numsubset])
            if (value=="positive"):#The case where negative file is classified as positive
               denominator+=1
            if (value=="negative"): #The case where file is correctly classified as negative
               numerator2+=1
               denominator2+=1
         precisionP.append(numerator*1.0/denominator) #Append to positive value precision list
         precisionN.append(numerator2*1.0/denominator2) #Append to negative value precision list

   def classifyTest(self, sText, dictP,dictN):
      """Improved Test for cross validation"""
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
      for value in (dictP).values():
         totalFreqP=totalFreqP+value
      
      # Find frequency of negative words
      totalFreqN=0
      for value in (dictN).values():
         totalFreqN=totalFreqN+value

      # Compute probabilityP for each file
      lst=self.tokenize(sText)
      for word in lst:
         wordFreq=0
         if (dictP).has_key(word):
            wordFreq=(dictP).get(word)
         else:
            wordFreq=1
         wordprob=wordFreq*1.0/(totalFreqP)
         probabilityP=probabilityP+math.log(wordprob*1.0)

      # Compute probabilityN for each file
      for word in lst:
         wordFreq=0
         if (dictN).has_key(word):
            wordFreq=(dictN).get(word)
         else:
            wordFreq=1 #Default frequency 1 if not found
         wordprob=wordFreq*1.0/(totalFreqN)
         probabilityN=probabilityN+math.log(wordprob*1.0)

      # Take absolute value of computed log probability
      probabilityP=abs(probabilityP)
      probabilityN=abs(probabilityN)

      stringLen=len(lst) # Get the number of strings in the input
      lensqt1=math.sqrt(stringLen)
      lensqt=math.sqrt(lensqt1) # Takes the 4th root of the number of strings

      if probabilityP>probabilityN:
         if (probabilityN>probabilityP-0.7*lensqt): #Use lensqt in our classification
            return "neutral" #Values are too close, return neutral
         else:
            return "negative" #More likely to be negative, return
      if probabilityP<=probabilityN:
         if (probabilityP>probabilityN-0.7*lensqt): #Use lensqt in our classification
            return "neutral" #Values are too close, return neutral
         else:
            return "positive" #More likely to be positive, return

   def classifyTestOrg(self, sText, dictP,dictN):
      """Original Test for cross validation"""
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
      for value in (dictP).values():
         totalFreqP=totalFreqP+value
      
      # Find frequency of negative words
      totalFreqN=0
      for value in (dictN).values():
         totalFreqN=totalFreqN+value

      # Compute probabilityP for each file
      lst=self.tokenize(sText)
      for word in lst:
         wordFreq=0
         if (dictP).has_key(word):
            wordFreq=(dictP).get(word)
         else:
            wordFreq=1
         wordprob=wordFreq*1.0/(totalFreqP)
         probabilityP=probabilityP+math.log(wordprob*1.0)

      # Compute probabilityN for each file
      for word in lst:
         wordFreq=0
         if (dictN).has_key(word):
            wordFreq=(dictN).get(word)
         else:
            wordFreq=1 #Default frequency 1 if not found
         wordprob=wordFreq*1.0/(totalFreqN)
         probabilityN=probabilityN+math.log(wordprob*1.0)

      # Take absolute value of computed log probability
      probabilityP=abs(probabilityP)
      probabilityN=abs(probabilityN)

      if probabilityP>probabilityN:
         if (probabilityN>probabilityP-0.8):
            return "neutral" #Return neutral since values are too close
         else:
            return "negative" #Return negative, more likely
      if probabilityP<=probabilityN:
         if (probabilityP>probabilityN-0.8):
            return "neutral" #Return neutral since values are too close
         else:
            return "positive" #Return negative, more likely

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