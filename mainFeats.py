import random
import time
import os
import msvcrt
import csv
from os import listdir
from os.path import isfile, join

locipath="./Loci"
datas="./rawDatas/feats.csv"
f2=open('./rawDatas/global.txt', 'a') #print globalMessages

class Feat:
    def __init__(self, nbRows, lengthColumn,memoTime,restiTime,sizeCell=None,separator="",separatorPlaceHolder=2,tempFile="temp.txt",indent=5,blocMode=False,revert=False):
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

    def proceed(self):
        self.build_table_solution()
        self.print_table(self.nbRows)
        print("\n"*9)
        time.sleep(self.memoTime)
        print("\n"*30)
        timeResti=time.clock()
        with open(self.tempFile, 'w') as f:
            pass
        os.system("start "+self.tempFile)# windows only, for mac : os.system("open "+filename)
        do=raw_input("quit (q), load the answer file(l) : ")
        if(do=="l"):
            timeElapsed=round(time.clock()-timeResti)
            self.answer=self.buildAnswerFromFile(self.tempFile)
            [errors,points,nlines]=self.compareSolutionAnswer(self.solution,self.answer)
            self.print_debrief(errors,points,nlines,timeElapsed)
        return self.solution,self.answer

    def print_debrief(self,errors,points,nl,timeElapsed):
        self.print_table(nl)
        print("\n")
        print("you got "+str(points)+" points")
        print("remaining restitution time : "+str(self.restiTime-timeElapsed))+" s"
        message2="feat : %s, memotime : %s, points : %s"%(str(self.__class__.__name__),str(self.memoTime),str(points))
        f2.write(message2)      
        for error in errors:
            print "at line %d,column %d you wrote %s instead of %s"  % (error[0], error[1],error[2],error[3])
                    

    def print_table(self,nR):
        print("\n"*(10+(20-nR)/2))
        lines=self.table.splitlines()
        if(self.revert):
            nR=len(lines)#dirty to avoid complications
        for l in range(nR):
            print(lines[l])
            
    def build_table_solution(self):
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
                item=str(self.generateItem())
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

    def buildAnswerFromFile(self,fname):
        answer=[]
        with open(fname, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                lanswer=[]
                if(self.blocMode):
                    lanswer.extend(row)
                else:
                    for element in row:
                        lanswer.extend(element)
                answer.append(lanswer)
        return answer
            
    def generateItem( self ):
        raise NotImplementedError( "Should have implemented generateItem" )

    def compareSolutionAnswer(self,lsol,lansw): 
        indexL=0
        points=0
        errors=[]
        if(self.revert): # columns are taken as lines in order to compare columns by columns
            lsol=zip(*lsol)
            lansw=zip(*lansw)
        for linAns in lansw:
            lineErrors=0
            indexCol=0
            for item in linAns:
                if(lsol[indexL][indexCol]!=item):
                    errorReport=[indexL,indexCol,item,lsol[indexL][indexCol]]
                    errors.append(errorReport)
                    lineErrors+=1
                indexCol+=1
            if lineErrors==1:
                points+=indexCol/2
            else:
                if lineErrors==0:
                  points+=indexCol  
            indexL+=1
        return(errors,points,indexL)
    


    
     

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

def reportDatas(sol,ans,system,globalReport,locis=None,checker="n",revert=False):
    if(revert): # columns are taken as lines in order to compare columns by columns
        sol=zip(*sol)
        ans=zip(*ans)
    fsol=[item for sublist in sol for item in sublist]#flatten sol
    fans=[item for sublist in ans for item in sublist]
    blocs=system["system"].split(",")
    currentLoci=""
    indexAns=0
    indexLoci=0
    cont=True
    localReport=[]
    spot=0
    #if loci is not defined, default values avoiding bugs
    if(locis==None):
        indexLoci=""
        currentLoci=["",""]
    while cont:
        for b,bloc in enumerate(blocs):
            if(locis!=None):
                #print(locis)
                #print(indexLoci)
                currentLoci=locis[indexLoci]
                indexLoci+=1
            for image in bloc:
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
                localReport.append([answer,solution,correct,image,currentLoci[0],currentLoci[1],b,indexLoci,spot])
                #print(answer,sol,currentLoci)
                indexAns+=size
    if(checker=="y")and(locis!=None):
        checked=raw_input("the last loci you used was %s, containing %s, right ? (y/n) : "%(currentLoci[1],solution))
        if(checked=="n"):
            raw_input("fix your loci csv files by adding or deleting locis, eventually with a csv temp file (must keep the loci id though) then push enter")
            locis=lociLoader()
            reportDatas(sol,ans,system,globalReport,locis,checker="y")
        else:
            printReports(globalReport,localReport)
    else:
        printReports(globalReport,localReport)


def printReports(globalReport,localReport):
    with open(datas, 'ab') as f:
        writer = csv.writer(f,delimiter=';')
        for l in localReport:
            l.extend(globalReport)
            writer.writerow(l)   

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
    while True:
        lociFiles = [ f for f in listdir(locipath) if (isfile(join(locipath,f))and f[-4:]==".csv" )]
        message="load options : "
        for i,lf in enumerate(lociFiles):
            message+="\n -"+lf+"("+str(i)+") "
        message+="\n choice : "
        il=raw_input(message)
        chosenFile=lociFiles[int(il)]
        fileName=join(locipath,chosenFile)
        updateUuid(fileName)
        locis=[]
        startingIndex=raw_input("starting index (default=0) : ")
        if(startingIndex!=""):
            startingIndex=int(startingIndex)
            
        if(startingIndex==""):
            startingIndex=0
            
        with open(fileName, 'rb') as csvfile: #read
            spamreader = csv.reader(csvfile, delimiter=';')
            for i,r in enumerate(spamreader):
                if(i>startingIndex-1):
                    locis.append(r)
        
        if(startingIndex!=0):
            okloc=raw_input('the first loci was "'+str(locis[startingIndex][1])+'" ok ? (y/n) (default=y): ')
            if(okloc!="n"):#if no, we continue to loop in loci selection
                break
        else:
            break
    return locis
            

if __name__ == "__main__":
    
    feat=raw_input("pick your feat (d=digits,b=binaries,w=words) : ")
    if(feat=="")or(feat=="d"):
        feat="d"
        sep,row,col,memoTime,restiTime,sepSign=2,20,40,300,900,"|"
        
    if(feat=="w"):
        freqMax=raw_input("N th Most frequent words (no if no limit, default=8000) : ")
        if(freqMax==""):
            freqMax=8000
        else:
            freqMax=int(freqMax)
        sep,row,col,memoTime,restiTime,sepSign=1,20,5,300,900,"|"
        
    if(feat=="b"):
        sep,row,col,memoTime,restiTime,sepSign=6,25,30,300,900,"|"
        
    else:
        sepN=raw_input("separaters every N items (default=%d) : "%sep)
        
    nr=raw_input("how many rows (default=%d) : "%row)
    nc=raw_input("how many cols (default=%d) : "%col)
    mt=raw_input("how much time (s) (default=%ds) : "%memoTime)
    rt=raw_input("how much time to write (s) (default=%ds) : "%restiTime)
    

    if (mt!=""):
        maxTime=float(mt)

    if (rt!=""):
        restiTime=float(rt)
        
    if (nr!=""):
        row=int(nr)

    if (nc!=""):
        col=int(nc)
        
    if(sepN!=""):
        sep=int(sepN)
  
    memoTime=2    
    #sep,row,col,memoTime,restiTime,sepSign=2,40,20,300,900
    if(feat=="b"):
        ff=Binaries(row, col,memoTime,restiTime,sepSign,sep,"bin_temp.txt",indent=5)
    if(feat=="w"):
        ff=Words(row, col,memoTime,restiTime,sepSign,sep,"word_temp.txt",indent=2,freqMax=freqMax,sizeCell=20)
    if(feat=="d"):
        ff=Numbers(row, col,memoTime,restiTime,sepSign,sep,"num_temp.txt",indent=5)
    [solution,answer]=ff.proceed()
    report=raw_input("report results (y/n) (default=n) : ")
    
    if(report=="y"):
        pr=raw_input("load profile (y/n) (default=n) : ")
        locis,systemDic=None,None
        if(pr=="y"):
            profile = dict(line.strip().split('=') for line in open('profile.properties'))
            key=""
            if(feat=="w"):
                key=str(feat)+str(row) # for words, the number of row is more relevant
            else :
                key=str(feat)+str(col)
            if(key in profile):
                system=profile[key]
                systemDic={}
                systemDic["system"]=system
                temp={}
                limages=list(set(system)-set(','))
                for image in limages:
                    temp[image]=profile[image]
                systemDic["imagesSize"]=temp
                
        lo=raw_input("load journey (y/n) (default=n) : ")
        checker="n"
        if(lo=="y"):
            locis=lociLoader()             
            checker=raw_input("proceed to loci checker (advised) (y/n) (default=y) : ")
            if(checker==""):
                checker="y"
        if(systemDic!=None):
            globalReport=[feat,str(row), str(col),str(memoTime),str(restiTime),sepSign,str(round(time.time()))]
            reportDatas(solution,answer,systemDic,globalReport,locis,checker,ff.revert)
        

