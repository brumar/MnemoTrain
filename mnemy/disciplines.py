import random
import time
import os
import csv
from os import listdir
from os.path import isfile, join
import uuid
from PygameExperiment import *
import MOL
from mnemy import tableImageGenerator as tgen
from mnemy import tableFacesGenerator as tgenF
from mnemy.utils import openFileMultipleOs
from mnemy.utils import smartRawInput
from mnemy.training import *
import pickle
import winsound



f2=open('./rawDatas/global.txt', 'a') #print globalMessages
soundpath="spokenNumbersAudioFiles/french/"
pickleTrainingSpoken="saveSpokenNumberGame.p"
pickleRt="saveRt_2.p"
csvReactionTime='./rawDatas/reactionTimes.csv'
csvReactionTime2='./rawDatas/reactionTimes2.csv'
recallDir="./recallMaterial/"

#these options should not be there : TODO: fix this


#===============================================================================
# FUNCTIONS
#===============================================================================

class Feat:
    """Class implementing the most important features of each feats
    """
    def __init__(self, nbRows, lengthColumn,memoTime,
                 restiTime,sizeCell=None,separator="",
                 separatorPlaceHolder=2,tempFile="temp.txt",indent=5,
                 blocMode=False,revert=False,longestStreak=False):
        self.nbRows = nbRows
        self.lengthColumn= lengthColumn
        self.memoTime = memoTime
        self.restiTime= restiTime
        self.sizeCell= sizeCell
        self.separator=separator
        self.separatorPlaceHolder=separatorPlaceHolder
        self.solution=[]
        self.answer=[]
        self.table=""#string representation of the solution
        self.indent=indent
        self.tempFile=recallDir+tempFile
        self.blocMode=blocMode
        self.revert=revert
        self.attempt=0
        self.longestStreak=longestStreak

    def proceed(self):
        """Proceed to the feat
        """
        self.displayLearningMaterial()
        self.recall()
        return self.solution,self.answer,self.attempt

    def recall(self):
        self.beforeRecall() #act as a hook for feats requiring some actions
        timeResti=time.clock()
        self.createAndOpenSheet()

        do=raw_input("quit (q), load the answer file(l) : ")
        if(do=="l"):
            timeElapsed=round(time.clock()-timeResti)
            self.answer=self.buildAnswerFromFile(self.tempFile)
            [errors,points,nlines,self.attempt]=self.compareSolutionAnswer(self.solution,self.answer)
            self.print_debrief(errors,points,nlines,timeElapsed)

    def beforeRecall(self):
        pass

    def displayLearningMaterial(self):
        self.waiter(self.nbRows)
        self.build_table_solution()
        self.print_table(self.nbRows)
        print("\n"*9)
        time.sleep(self.memoTime)
        print("\n"*30)


    def waiter(self,nR):
        time.sleep(1)
        self.printNumber("3")
        time.sleep(1)
        self.printNumber("2")
        time.sleep(1)
        self.printNumber("1")
        time.sleep(1)

    def printNumber(self,ms):
        print "\n" * 20
        print "            "+ms
        print "\n" * 19

    def createAndOpenSheet(self):
        """ Open a temp file as a recall sheet
        """
        with open(self.tempFile, 'w') as f:
            pass
        openFileMultipleOs(self.tempFile)# windows only, for mac : os.system("open "+filename)

    def buildAnswerFromFile(self,fname):
        """ Read the recall file given by the user """
        answer=[]
        with open(fname, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            for row in spamreader:
                lanswer=[]
                if(self.blocMode):
                    lanswer.extend(row)
                else:
                    for element in row:
                        lanswer.extend(element)
                answer.append(lanswer)
        return answer

    def compareSolutionAnswer(self,lsol,lansw):
        """ compare the recall file with the target, count the points and raise the errors"""
        indexL=0
        points=0
        errors=[]
        attempt=0
        noError=True #usefull for speed cards only
        LstStreak=-1
        if(self.revert): # columns are taken as lines in order to compare columns by columns
            lsol=zip(*lsol)
            lansw=zip(*lansw)
        for linAns in lansw:
            lineErrors=0
            indexCol=0
            for item in linAns:
                attempt+=1
                if(lsol[indexL][indexCol]!=item):
                    errorReport=[indexL,indexCol,item,lsol[indexL][indexCol]] #TODO: should be a class
                    errors.append(errorReport)
                    if( noError):
                        LstStreak=attempt-1
                        noError=False
                    lineErrors+=1
                indexCol+=1
            if lineErrors==1:
                points+=indexCol/2
            else:
                if lineErrors==0:
                    points+=indexCol
            indexL+=1
            if(self.longestStreak):
                points=LstStreak
        return(errors,points,indexL,attempt)

    def print_debrief(self,errors,points,nl,timeElapsed):
        """ Display User friendly outputs
        """
        self.globalMessages(nl,points,timeElapsed)
        self.printErrors(errors)

    def printErrors(self,errors):
        for error in errors:
            if(len(error)==4):
                print "at line %d,column %d you wrote %s instead of %s"  % (error[0], error[1],error[2],error[3])
            elif (len(error)==3):
                print "at line %d you wrote %s instead of %s"  % (error[0], error[1],error[2])

    def globalMessages(self,nl,points,timeElapsed):
        self.print_table(nl)
        print("\n")
        print("you got "+str(points)+" points")
        print("remaining restitution time : "+str(self.restiTime-timeElapsed)+" s")
        print("if you load your profile, you can get more readable reports")
        message2="feat : %s, memotime : %s, points : %s \n"%(str(self.__class__.__name__),str(self.memoTime),str(points))
        f2.write(message2)

    def print_table(self,nR):
        """ Display the table of the elements to be learned
        """
        print("\n"*(10+(20-nR)/2))
        lines=self.table.splitlines()
        if(self.revert):
            nR=len(lines)#dirty to avoid complications
        for l in range(nR):
            print(lines[l])

    def build_table_solution(self):
        """ Build the displayed table of the items to be learned
            and build the solution vector"""

        self.solution=[] # might be redundant
        self.table=""
        for r in range(self.nbRows):
            solutionline=[]
            row=" "*self.indent
            for l in range(self.lengthColumn):
                sep=""
                if(self.separator!=""):
                    if(l%self.separatorPlaceHolder==0):
                        sep=self.separator
                item=str(self.generateItem())       # use generateItem which must be implemented in inherited classes
                solutionline.append(item)
                if(self.sizeCell!=None):
                    decalTotal=self.sizeCell-len(item)
                    decalLeft=decalTotal/2
                    decalRight=decalTotal-decalLeft
                    row+=sep+" "*decalLeft+item+" "*decalRight
                else:
                    row+=sep+item
            self.table+=row+sep+"\n"
            self.solution.append(solutionline)

    def update_table_solution(self): # dirty and incomplete
        """ Rebuild the displayed table according to the current solution vector"""
        self.table=""
        sep=self.separator
        for solutionline in self.solution:
            row=""
            for item in solutionline:
                row+=sep+item
            self.table+=row+sep+"\n"



class Dates(Feat):
    def __init__(self, nbRows, lengthColumn,memoTime,restiTime,separator="|",separatorPlaceHolder=2,tempFile="temp.txt",indent=5,freqMax=8000,dico='./dates/dates.csv',sizeCell=20,blocMode=True,revert=True):
        Feat.__init__(self, nbRows, lengthColumn,memoTime,restiTime,sizeCell,separator,separatorPlaceHolder,tempFile,indent,blocMode=True)
        self.dates=[]
        self.readDic(dico)#put 2 extra arguments + sizecell=20
    def readDic(self,dictionnary):
        with open(dictionnary, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for r,row in enumerate(spamreader):
                self.dates.extend(row)

    def generateItem(self):
        date=str(random.randint(1000, 2099))
        label=random.choice(self.dates)
        return date+self.separator+label

    def createAndOpenSheet(self): #overriding default method
        with open(self.tempFile, 'wb') as f:
            dates=[]
            random.shuffle(self.solution)#recall sheet is shuffled !
            self.update_table_solution()#update table accordingly
            for l in self.solution:
                datelabel=l[0][4:]
                date=l[0][:4]
                dates.append(date)
                f.write(datelabel+'\n')
            self.solution=dates
        openFileMultipleOs(self.tempFile)# windows only, for mac : os.system("open "+filename)

    def buildAnswerFromFile(self,fname):
        answer=[]
        with open(fname, 'rb') as f:
            for line in f:
                answer.append(line[:4])
        return answer

    def compareSolutionAnswer(self,lsol,lansw): #override
        indexL=0
        points=0
        errors=[]
        atempt=0
        for linAns in lansw:
            lineErrors=0
            indexCol=0
            date=""
            for digit in linAns:
                date+=digit
                if digit==self.separator:
                    break
            if(date!=self.separator):
                atempt+=1
                if(lsol[indexL]!=date):
                    errorReport=[indexL,date,lsol[indexL]]
                    errors.append(errorReport)
                    lineErrors+=1
                else:
                    points+=1
            indexL+=1
        return(errors,points,indexL,atempt)

class Numbers(Feat):
    def __init__(self, nbRows=1, lengthColumn=1,memoTime=300,restiTime=1500,separator="|",separatorPlaceHolder=2,tempFile="temp.txt",indent=5,sizeCell=None,blocMode=False):
        Feat.__init__(self, nbRows, lengthColumn,memoTime,restiTime,sizeCell,separator,separatorPlaceHolder,tempFile,indent,blocMode)

    def generateItem(self):
        return random.randint(0, 9)

    def trainingGame(self,mode="amort"): # TODO: some functions must be taken from a parent class reserved for reaction time training
        if(mode=="amort"):
            dics=profileLoaderForReactionTraining('user/profile.properties','d')
            loadSet="n"
            if(len(dics)!=0):
                loadSet = smartRawInput('we have found special settings for this feat, load (y/n)',"y")
                if(loadSet=="y"):
                    listOfSystem=[system["system"] for system in dics] # get the systems as a list 
                    pick=multipleChoice(listOfSystem) # user has multiple choice
                    selectedSystem=dics[pick] # ... no pun intended
            f1=open(csvReactionTime2, 'a')
            nbDigits=-1 #value by default to avoid bug
            if(loadSet!="y"):
                raw_input('no system for this feat has been selected, but you can work on single items push enter')
                nbDigits = smartRawInput('how many digits ? ',"2",int)
                # COULD BE IMPROVED TO CREATE A SYSTEM
                letter = smartRawInput('write a single letter to represent this system (keep the same letter later) ',"Z")
                selectedSystem={'imagesSize': {letter: str(nbDigits)}, 'system': letter}
            coef=smartRawInput("attenuation coefficient in %",25,float)
            meta_coef=smartRawInput("meta attenuation coefficient in %",5,float)
            meta_coef=1+float(meta_coef)/100
            c=1+float(coef)/100                 
            t=smartRawInput("how much practice in seconds",180,float)
            inhib=smartRawInput("minimal gap between items",3,int)
            sepSign=smartRawInput("separator between numbers(n for none)","|")
            if(sepSign=="n"):
                sepSign=""
            record = smartRawInput('record data (y/n)',"y")
            lastIt=lastItems(inhib)
            
            try:
                controlStructure = pickle.load( open( pickleRt, "rb" ) )
            except : # if no data stored start with a home made dictionnary
                controlStructure=None
            if((controlStructure==None)or(selectedSystem['system'] not in controlStructure["system"])): # the way to get system wont work with digits only
                # if a system is already in we do not update, can cause problem if the system of the user is updated
                controlStructure=buildAStructure(controlStructure,selectedSystem,mode="d")
                controlStructure["infos"]["compteur"]=controlStructure["infos"]["compteur"]+1
            
            trials=0
            waiter()
            startExp=time.clock()
            
            ######## TRAINING LOOP ########
            
            while(True):
                startTrial= time.clock()
                trials+=1
                items,lastIt = displayItemForTrainingRT(lastIt, controlStructure,selectedSystem,nbDigits,sepSign)
                Userinput=raw_input("")
                nt=time.clock()
                if (Userinput=="q")or((nt-startExp)>t):
                    pickle.dump( controlStructure, open( pickleRt, "wb" ) )
                    print("during your training during %d s, you have seen %d items"%(t,trials))
                    printSumStruc(controlStructure,selectedSystem)
                    break
                timeElapsed=nt-startTrial
                timeElapsed_tosend=timeElapsed
                if(timeElapsed>6)or(timeElapsed<0.3):
                    timeElapsed_tosend=-1
                if(record=="y")and(timeElapsed_tosend!=-1):
                    controlStructure=updateControlStructure(controlStructure,selectedSystem,nbDigits,items,timeElapsed_tosend,c,meta_coef)
                    f1.write(str(controlStructure["infos"]["compteur"])+";"+selectedSystem['system']+";"+str(trials)+";"+str(time.time())+";"+str(timeElapsed)+";"+"".join(items)+ ";geometricOdd;"+str(inhib)+";"+str(c)+";"+str(meta_coef)+";"+str(t)+"\n")


class SpokenNumbers(Feat):  # TODO: much
    def __init__(self, nbRows=1, lengthColumn=1,memoTime=1,restiTime=900,separator="|",separatorPlaceHolder=2,tempFile="temp.txt",indent=5,sizeCell=None,blocMode=False):
        Feat.__init__(self, nbRows, lengthColumn,memoTime,restiTime,sizeCell,separator,separatorPlaceHolder,tempFile,indent,blocMode)

    def generateItem(self):
        return random.randint(0, 9)

    def beep(self,sound):
        winsound.PlaySound(soundpath+'%s.wav' % sound, winsound.SND_FILENAME)

    def displayLearningMaterial(self,n,f):
        answer=""
        t0= time.clock()
        for x in range(0,n):
            while True:
                nt=time.clock()
                if(nt - t0>f):
                    t0=nt
                    break
            m=str(self.generateItem())
            answer+=m
            sound=m
            self.beep(sound)
        self.solution=answer

    def trainingGame(self):
        N=smartRawInput("how many numbers",12,int)
        fstep=smartRawInput("which freq step",0.04,float)
        threshold=smartRawInput("max deviation (s) before increasing/decreasing numbers",0.15,float)
        Ninc=smartRawInput("how many numbers are added when threshold is reached",6,int)
        freq=1
        while True:
            self.displayLearningMaterial(N,freq)
            ans=raw_input("your answer : ")
            if(self.solution!=ans):
                freq+=fstep
                print("wrong")
                print("the solution: %s"%(self.solution))
                if(abs(freq-1)>threshold)and(N-Ninc>0):
                    if(N-Ninc>0):
                        N=N-Ninc
                        freq=1
                        print("Threshold reached : settings are now %.2f for %d items"%(freq,N))
                        
            else:
                print("success")
                freq-=fstep
                if(abs(freq-1)>threshold):
                    N=N+Ninc
                    freq=1
                    print("Threshold reached : settings are now %.2f for %d items"%(freq,N))                                        
            print("current freq : %.2f "%(freq))
            d=raw_input("enter to continue, q to quit : ")
            if(d=="q"):
                print("you stopped at %.2f for %d items"%(freq,N))
                return

class Binaries(Feat):
    def __init__(self, nbRows, lengthColumn,memoTime,restiTime,separator="|",separatorPlaceHolder=2,tempFile="temp.txt",indent=5,sizeCell=None,blocMode=False):
        Feat.__init__(self, nbRows, lengthColumn,memoTime,restiTime,sizeCell,separator,separatorPlaceHolder,tempFile,indent,blocMode)

    def generateItem(self):
        return random.randint(0, 1)

class Words(Feat):
    def __init__(self, nbRows, lengthColumn,memoTime,restiTime,separator="|",separatorPlaceHolder=2,tempFile="temp.txt",indent=5,freqMax=8000,dico='./dictionnaries/french/newDic2.csv',sizeCell=20,blocMode=True,revert=True):
        Feat.__init__(self, nbRows, lengthColumn,memoTime,restiTime,sizeCell,separator,separatorPlaceHolder,tempFile,indent,blocMode,revert)
        self.nouns=[]
        self.verbs=[]
        self.readDic(dico,freqMax)#put 2 extra arguments + sizecell=20
        #revert

    def readDic(self,dictionnary,freqMax):
        with open(dictionnary, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for r,row in enumerate(spamreader):
                if(r==freqMax):
                    break
                if(row[0]=="n"):
                    self.nouns.append(row[1])
                if(row[0]=="v"):
                    self.verbs.append(row[1])

    def generateItem(self):
        if(random.randint(0, 9)==9):
            return random.choice(self.verbs)
        else:
            return random.choice(self.nouns)

class Cards(Feat, PygameExperiment):
    def __init__(self,row=1, col=1, memoTime=300,restiTime=900,sep=2,tempFile="temp.txt",manyDecks=False):
        longestStreak=(row==1)# points counting differs for speed cards
        Feat.__init__(self, row, col,memoTime,restiTime,separatorPlaceHolder=sep,tempFile="cards_temp.txt",blocMode=True,longestStreak=longestStreak)
        PygameExperiment.__init__(self, filename=None, subject = "John Doe", debug = False,system="PA",manyDecks=manyDecks,sep=sep)

    def displayLearningMaterial(self):
        self.explore()
        self.ending()
        self.solution=self.solution   # dirty trick to get solution vector consistent with comparison algo

    def print_table(self,nR):
        print(str(self.solution))#completely lame \O/
        #TODO: Better print table with unicode playing cards

    def globalMessages(self,nl,points,timeElapsed):
        self.print_table(nl)
        print("\n")
        t=str(float(self.viewingTime)/1000)
        if(points!=-1):
            print("you got "+str(points)+" points")
        else:
            print("perfect recall in "+t+"s")
        print("remaining restitution time : "+str(self.restiTime-timeElapsed)+" s")
        print("if you load your profile, you can get more readable reports")
        message2="feat : %s, memotime : %s, points : %s , time : %s \n"%(str(self.__class__.__name__),str(self.memoTime),str(points),t)
        f2.write(message2)

    def trainingGame(self):
        self.prepareDeck()
        self.trainingRT()
        self.ending()

class AbstractImages(Feat):
    def __init__(self, nbRows, lengthColumn,memoTime,restiTime,blocMode=True):
        Feat.__init__(self, nbRows, lengthColumn,memoTime,restiTime,blocMode=blocMode,tempFile="images_temp.txt")
        self.imageFiles=[]
        self.buildCollection("./abstractImages")#put 2 extra arguments + sizecell=20
        self.tableRepresentation=[]
        self.tableRepresentationRecall=[]
        self.path="../abstractImages/"

    def beforeRecall(self):
        self.shuffleTable()
        recallsheet="./recallMaterial/recall.html"
        tgen.createTemplate(self.tableRepresentationRecall,recallsheet,self.path)
        openFileMultipleOs(recallsheet)
        self.buildSolution()

    def buildSolution(self):
        self.solution=[]
        for r,row in enumerate(self.tableRepresentationRecall):
            v=[]
            for image in row:
                newIndex=(self.tableRepresentation[r]).index(image)
                v.append(str(newIndex+1))
            self.solution.append([",".join(v)])

    def shuffleTable(self):
        for row in self.tableRepresentation:
            rowtemp=list(row) # cloning to avoid shuffling the original list
            rd.shuffle(rowtemp)
            self.tableRepresentationRecall.append(rowtemp)

    def print_table(self,nR):
        pass

    def buildCollection(self,imagePath):
        self.imageFiles = [ f for f in listdir(imagePath) if (isfile(join(imagePath,f)) )]
        rd.shuffle(self.imageFiles)

    def displayLearningMaterial(self):
        self.tableRepresentation=self.buildTable()
        sheetName="./recallMaterial/learn.html"
        tgen.createTemplate(self.tableRepresentation,sheetName,self.path)
        openFileMultipleOs(sheetName)# windows only, for mac : os.system("open "+filename)
        time.sleep(self.memoTime)

    def buildTable(self):
        ta=[]
        for r in range(self.nbRows):
            t=[]
            for c in range(self.lengthColumn):
                t.append(self.imageFiles.pop())
            ta.append(t)
        return ta

class NameAndFaces(Feat):
    def __init__(self, nbRows, lengthColumn,memoTime,restiTime,blocMode=True,rankMax=10000):
        Feat.__init__(self, nbRows, lengthColumn,memoTime,restiTime,tempFile="faces_temp.txt")
        self.rankMax=rankMax
        self.imageMaleFiles=[]
        self.imageFemaleFiles=[]
        self.buildCollection("./faces/FemaleFaces/","./faces/MaleFaces/")#put 2 extra arguments + sizecell=20
        self.maleNames=self.buildNames("./names/MaleNames.csv")
        self.FemaleNames=self.buildNames("./names/FemaleNames.csv")
        self.allNames=[]
        self.allNames.extend(self.maleNames)
        self.allNames.extend(self.FemaleNames)
        self.sheetName="recallMaterial/learnFaces.html"
        self.solution={}
        self.imageToNames={}
        self.solutionAsImages={}
        self.tableImage=[]
        self.tableImageRecall=[]
        self.path="../faces/"

    def bindNamesToImages(self):
        ta=[]
        for r in range(self.nbRows):
            t=[]
            tima=[]
            for c in range(self.lengthColumn):
                name=random.choice(self.allNames)
                if(random.randint(0, 1)==0):
                    image=self.imageFemaleFiles.pop()
                    firstName=random.choice(self.FemaleNames)
                else:
                    image=self.imageMaleFiles.pop()
                    firstName=random.choice(self.maleNames)
                self.imageToNames[image]=[firstName,name]
                tima.append(image)
                t.append([image,firstName,name])
            self.tableImage.append(tima)
            ta.append(t)
        return ta

    def beforeRecall(self):
        self.shuffleTable()#self.tableImageRecall
        self.prepareImageRecall()
        recallsheet="./recallMaterial/recall.html"
        tgenF.createTemplate(self.tableImageRecall,recallsheet,self.path)
        openFileMultipleOs(recallsheet)
        self.buildSolution()

    def prepareImageRecall(self):
        index=0
        for r in range(self.nbRows):
            for c in range(self.lengthColumn):
                index+=1
                image=self.tableImageRecall[r][c]
                self.tableImageRecall[r][c]=[image,"",str(index)] #dirty trick to be template compliant in html generation

    def buildNames(self,dictionnary):
        l=[]
        with open(dictionnary, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for r,row in enumerate(spamreader):
                if(r==self.rankMax):
                    break
                l.append(row[0].title())#first letter in uppercase
        return l

    def buildSolution(self):#bind two dictionnaries together
        for ind,im in self.solutionAsImages.iteritems():
            vecNames=self.imageToNames[im]
            self.solution[ind]=vecNames

    def shuffleTable(self):
        temp=[item for sublist in self.tableImage for item in sublist]
        random.shuffle(temp)
        index=0

        self.tableImageRecall=[]
        for r in range(self.nbRows):
            ro=[]
            for c in range(self.lengthColumn):
                im=temp[index]
                ro.append(im)
                index+=1
                self.solutionAsImages[index]=im
            self.tableImageRecall.append(ro)

    def print_table(self,nR):
        pass

    def buildCollection(self,imageFemalePath,imageMalePath):
        self.imageMaleFiles = [ "MaleFaces/"+f for f in listdir(imageMalePath) if (isfile(join(imageMalePath,f)) )]
        self.imageFemaleFiles = [ "FemaleFaces/"+f for f in listdir(imageFemalePath) if (isfile(join(imageFemalePath,f)) )]
        rd.shuffle(self.imageMaleFiles)
        rd.shuffle(self.imageFemaleFiles)

    def displayLearningMaterial(self):
        self.nameAndFaces=self.bindNamesToImages()
        tgenF.createTemplate(self.nameAndFaces,self.sheetName,self.path)
        openFileMultipleOs(self.sheetName)# windows only, for mac : os.system("open "+filename)
        time.sleep(self.memoTime)

    def createAndOpenSheet(self): #overriding default method
        with open(self.tempFile, 'wb') as f:
            for indexImage in range(self.nbRows*self.lengthColumn):
                f.write(str(indexImage+1)+';\n')
        openFileMultipleOs(self.tempFile)# windows only, for mac : os.system("open "+filename)

    def buildAnswerFromFile(self,fname):
        answer={}
        try:
            with open(fname, 'rb') as f:
                for line in f:
                    if(not line.isspace()):                     
                        ansVec=line.split(";")
                        ansVec[1]=ansVec[1].replace("\n","")
                        if(ansVec[1]!=""):
                            answer[int(ansVec[0])]=ansVec[1].title().split(" ") #first letter uppercase even if the user forget it
        except:
            raise Exception("problem with your file")

        return answer

    def compareSolutionAnswer(self,lsol,lansw): #Here sol and lansw are dictionnaries
        points=0
        errors=[]
        attempts=0
        for index,vecNames in lansw.iteritems():
            noFault=True
            for position,name in enumerate(vecNames):
                attempts+=1
                if(lsol[index][position]==name):
                    points+=1
                else:
                    noFault=False
                    er=[index,1,str(lansw[index]),str(lsol[index])]
            if(not noFault):
                errors.append(er)

        return(errors,points,index,attempts)
