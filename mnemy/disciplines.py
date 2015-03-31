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

locipath="./Loci"
datas="./rawDatas/feats.csv"
f2=open('./rawDatas/global.txt', 'a') #print globalMessages

#these options should not be there : TODO: fix this


#===============================================================================
# FUNCTIONS
#===============================================================================
def find(l, elem):
    for row, i in enumerate(l):
        try:
            column = i.index(elem)
        except ValueError:
            continue
        return row, column
    return -1

def reportDatas(sol,ans,system=None,errorDic=None,globalReport=None,locis=None,revert=False): #too complex
    if(revert): # columns are taken as lines in order to compare columns by columns
        sol=zip(*sol)
        ans=zip(*ans)
    fsol=[item for sublist in sol for item in sublist]#flatten sol
    fans=[item for sublist in ans for item in sublist]
    currentLoci=""
    indexAns=0
    indexLoci=0
    cont=True
    localReport=[]
    spot=0
    if(system==None): #if uniBloc is true, it means that errors can be processed one by one (1 item = 1 image)
        blocs=["_"]
        size=1
    else:
        blocs=system["system"].split(",")
    if(locis==None):
        indexLoci=0
        currentLoci=["",""]
    while cont:
        for b,bloc in enumerate(blocs):
            if(locis!=None):
                currentLoci=locis[indexLoci]
                indexLoci+=1
            for image in bloc:
                if(system!=None):
                    size=int(system["imagesSize"][image])
                if(indexAns+size>len(fans)):
                    cont=False
                    break
                spot+=1
                answer=fans[indexAns:indexAns+size]
                solution=fsol[indexAns:indexAns+size]
                answer=''.join(answer)
                solution=''.join(solution)
                correct=(answer==solution)
                er=""
                if(correct==False):
                    if(errorDic!=None):
                        er=labelError(errorDic,currentLoci,indexLoci,image,solution,answer)
                localReport.append([answer,solution,correct,er,image,currentLoci[0],currentLoci[1],b,indexLoci,spot])
                indexAns+=size
        printReports(globalReport,localReport)


def labelError(errorDic,currentLoci,indexLoci,image,solution,answer):
    message=errorsPickerMessage(errorDic)+"\n you can also write a new error \n"
    print(message)
    print("Error : at %s (loci %d), %s was %s, not %s"%(currentLoci[1],indexLoci,image,solution,answer) )
    er=raw_input("your choice : ")
    try:
        ide=int(er)
        if ide in (errorDic["index"]).keys():
            er=errorDic["index"][ide]
    except : # case : a new error is written
        pass
    return er

def loadAndCheckJourney(systemDic,answer):
    while True:
        locis=lociLoader()
        status=lociChecker(locis,systemDic,answer)
        if(status=="y"):
            return locis
        if(status=="noloci"):
            return None
        else:
            option=raw_input("fix your loci csv files by adding or deleting locis, eventually with a csv temp file (must keep the loci id though) then push enter, write q to quit")
            if(option=="q"):
                return None

def lociChecker(locis,system,answer):
    answer=[item for sublist in answer for item in sublist]
    decision="y"
    if(system==None):
        decision=raw_input("no system for this feat ; one item by loci ? (y/n) (default=n) : ")
        if decision!="n":
            blocs=["_"]
        else:
            return "noloci"
    else:
        blocs=system["system"].split(",")
    lastThingStored,indexLoci=findLastLociLastItem(blocs,answer,system)
    try:
        lastLoci=locis[indexLoci]
    except:
        print("your journey seems too short for this feat")
        return "n"

    checked=raw_input("the last loci you used was %s, containing %s, right ? (y/n) (default=y) : "%(lastLoci[1],lastThingStored))#lastLoci = Trick to avoid strange bug
    if(checked==""):
        return "y"
    return checked

def findLastLociLastItem(blocs,answer,system):
    cursorAnswer=0;
    indexLoci=0;
    cont=True
    while cont:
        for bloc in blocs:
            for image in bloc:
                if(system!=None):
                    size=int(system["imagesSize"][image])
                else:
                    size=1
                if (cursorAnswer+size)<len(answer):
                    cursorAnswer+=size# more than one item can be stored ....
                    lastThingStored=answer[cursorAnswer:cursorAnswer+size]
                    lastThingStored=''.join(lastThingStored)
                else:#we set everything to break all the loops
                    return lastThingStored,indexLoci
            indexLoci+=1 # in only one loci

def printReports(globalReport,localReport):
    with open(datas, 'ab') as f:
        writer = csv.writer(f,delimiter=';')
        for l in localReport:
            l.extend(globalReport)
            writer.writerow(l)
    print("\n congratulations, the report has appended to "+datas)

def updateUuid(fileName):
    l=[]
    with open(fileName, 'rb') as csvfile: #read
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            #print(row)
            lr=[]
            if(len(row)==1):
                lr.append(str(uuid.uuid1()))
                lr.append(row[0])
            else:
                lr.extend(row)
            l.append(lr)

    with open(fileName, 'wb') as f: #overwrite
        writer = csv.writer(f,delimiter=';')
        for lr in l:
            writer.writerow(lr)


def lociLoader():
    lociFiles = [ f for f in listdir(locipath) if (isfile(join(locipath,f))and f[-4:]==".csv" )]
    message="load options : "
    for i,lf in enumerate(lociFiles):
        message+="\n -"+lf+"("+str(i)+") "
    message+="\n quit loading locis (q)"
    message+="\n choice : "
    il=raw_input(message)
    if il=="q":
        return None
    chosenFile=lociFiles[int(il)]
    fileName=join(locipath,chosenFile)
    updateUuid(fileName)
    locis=buildLociFromFile(fileName)
    specific=raw_input("this journey contains %d locis, do you want to start at a specific loci (y/n) default=n : "%len(locis))
    cp=1
    if(specific=="y"):
        message="index : "
        for indexLoc,loc in enumerate(locis):
            message+="\n -"+loc[1]+"("+str(indexLoc+1)+") "
        message+="\n choice : "
        chosenPosition=raw_input(message)
        cp=int(chosenPosition)
    return locis[cp-1:]

def buildLociFromFile(filename):
    locis=[]
    with open(filename, 'rb') as csvfile: #read
        spamreader = csv.reader(csvfile, delimiter=';')
        for i,r in enumerate(spamreader):
            locis.append(r)
        return locis


def profileLoader(profileFile,feat,row,col):
    systemDic={}
    try:
        profile = dict(line.strip().split('=') for line in open(profileFile))
    except:
        raise Exception(profileFile+" not found")
    key=""
    if(feat=="w"):
        key=str(feat)+str(row) # for words, the number of row is more relevant
    else :
        key=str(feat)+str(col)
    if(key in profile):
        system=profile[key]
        systemDic["system"]=system
        temp={}
        limages=list(set(system)-set(','))
        for image in limages:
            try:
                temp[image]=profile[image]
            except:
                raise Exception("no size affected to "+image)
        systemDic["imagesSize"]=temp
    else:
        raise Exception("no system for this feat")
    return systemDic

def errorsLoader(errorsFile):
    errors={}
    try:
        errors = dict(line.strip().split('=') for line in open(errorsFile))
    except:
        raise Exception(errorsFile+" not found")
    errors["index"]={}
    for e,error in enumerate(errors.keys()):
        if(e!="index"):
            errors["index"][e]=error;
        # this dic is usefull for letting the user pick an error with an index
    return errors

def errorsPickerMessage(errorsDic): #message is "describe" or "select"
    # TODO:  an enumeration would be better
    message=""
    for error,description in errorsDic.iteritems():
        if(error!="index"):
            message+="%s : %s \n"%(error,description)
    message+="\n"
    for i,error in (errorsDic["index"]).iteritems():
        message+="%s (%d)\n"%(error,i)
    return message

#===============================================================================
# CLASSES
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
        self.tempFile=tempFile
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
    def __init__(self, nbRows, lengthColumn,memoTime,restiTime,separator="|",separatorPlaceHolder=2,tempFile="temp.txt",indent=5,freqMax=8000,dico='./dates/13jan.csv',sizeCell=20,blocMode=True,revert=True):
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
    def __init__(self, nbRows, lengthColumn,memoTime,restiTime,separator="|",separatorPlaceHolder=2,tempFile="temp.txt",indent=5,sizeCell=None,blocMode=False):
        Feat.__init__(self, nbRows, lengthColumn,memoTime,restiTime,sizeCell,separator,separatorPlaceHolder,tempFile,indent,blocMode)

    def generateItem(self):
        return random.randint(0, 9)

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
    def __init__(self,row, col, memoTime,restiTime,sep,tempFile="temp.txt",manyDecks=False):
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

class AbstractImages(Feat):
    def __init__(self, nbRows, lengthColumn,memoTime,restiTime,blocMode=True):
        Feat.__init__(self, nbRows, lengthColumn,memoTime,restiTime,blocMode=blocMode,tempFile="images_temp.txt")
        self.imageFiles=[]
        self.buildCollection("./abstractImages")#put 2 extra arguments + sizecell=20
        self.tableRepresentation=[]
        self.tableRepresentationRecall=[]
        self.path="abstractImages"

    def beforeRecall(self):
        self.shuffleTable()
        recallsheet="recall.html"
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
        sheetName="learn.html"
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
        self.sheetName="learnFaces.html"
        self.solution={}
        self.imageToNames={}
        self.solutionAsImages={}
        self.tableImage=[]
        self.tableImageRecall=[]
        self.path="faces"

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
        recallsheet="recall.html"
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