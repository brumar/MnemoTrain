import time
import random as rd
import itertools
import operator
import math
from utils import writeLongMessageInFile,openFileMultipleOs
import csv
import uuid
from os import listdir
from os.path import isfile, join

locipath="./user/Loci"
datas="./rawDatas/feats.csv"

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

def printReports(globalReport,localReport,datas):
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



def multipleChoice(alist):
    """
    Let the user choose amongst many actions, the index of a list is returned
    """
    message = "load options : "
    for i, lf in enumerate(alist):
        message += "\n -" + lf + "(" + str(i) + ") "
    
    message += "\n quit loading (q)"
    message += "\n choice : "
    il = raw_input(message)
    if il=="q":
        return None
    return int(il)

def lociLoader(locipath):
    lociFiles = [ f for f in listdir(locipath) if (isfile(join(locipath,f))and f[-4:]==".csv" )]
    index = multipleChoice(lociFiles)
    chosenFile=lociFiles[index]
    fileName=join(locipath,chosenFile)
    updateUuid(fileName)
    locis=buildLociFromFile(fileName)
    specific=raw_input("this journey contains %d locis, do you want to start at a specific loci (y/n) default=n : "%len(locis))
    cp=1
    message=""
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
    """ Load the profile file of the user into a dictionnary 
    Keyword arguments:
    profileFile -- the path to the profile file
    feat -- the feat to inspect
    row -- the number of rows for this feat
    col -- the number of rows for this feat
    Return a dic with two keys imagesSize (a dic) and system (the name of the system)
    
    TODO:Recent (untested) modifications
    """

    profile=openProfile(profileFile)
    key=""
    if(feat=="w"):
        key=str(feat)+str(row) # for words, the number of row is more relevant
    else :
        key=str(feat)+str(col)
    if(key in profile):
        return createSystem(key,profile[key],profile)

def openProfile(profileFile):
    try:
        profile = dict(line.strip().split('=') for line in open(profileFile))
    except:
        raise Exception(profileFile+" not found")
    return profile

def profileLoaderForReactionTraining(profileFile,feat):
    """ Load the profile file of the user into a dictionnary 
    Keyword arguments:
    profileFile -- the path to the profile file
    feat -- the feat to inspect
    Return a list of dic with two keys imagesSize (a dic) and system (the name of the system)
    """
    systemsDic=[]
    profile=openProfile(profileFile)
    for key in profile:
        if(key.startswith("rt_"+feat)):
            systemsDic.append(createSystem(key,profile))
    return systemsDic

def createSystem(key,profile):
    """Return a list of dic with two keys imagesSize (a dic) and system (the name of the system)
    """
    systemDic={}
    systemAsString=profile[key]
    systemDic["system"]=systemAsString
    temp={}
    limages=list(set(systemAsString)-set(','))
    for image in limages:
        try:
            temp[image]=profile[image]
        except:
            raise Exception("no size affected to "+image)
    systemDic["imagesSize"]=temp
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



class lastItems:
    def __init__(self,Nmax):
        self.Nmax=Nmax
        self.list=[]

    def add(self,item):
        if (len(self.list)==self.Nmax):
            self.list.pop(0)
            self.list.append(item)
        else:
            self.list.append(item)

    def contains(self,newItem):
        return (newItem in self.list)




def printNumber(ms):
    print "\n" * 20
    print "            "+ms
    print "\n" * 19

def waiter():
    time.sleep(1)
    printNumber("3")
    time.sleep(1)
    printNumber("2")
    time.sleep(1)
    printNumber("1")
    time.sleep(1)
    

def turnIntoPrintableString(item,nbDigits=2):
    item = "0" * (nbDigits - len(str(item))) + str(item)
    return item

def takeItems(currentDic,lastIt,sys,mode):
    items=[]
    for image in sys:
        item=takeItem(currentDic[image],lastIt)
        lastIt.add(item)
        items.append(item)      
    return items,lastIt

def takeItem(dic,lastIt):
    while True:# loop related to last Item checking
        r=rd.random()
        cumul=0
        for item,proba in dic["probas"].iteritems():
            try:
                cumul+=proba #out of range can occur...
            except:
                return takeItem(dic,lastIt)# in this case the function is called again
            if(r<cumul):
                if(not lastIt.contains(item)): #...because of this filter
                    return item

 
def updateControlStructure(controlStructure,selectedSystem,nbDigits,items,timeElapsed_tosend,c,meta_coef):
    sys=selectedSystem["system"]
    currentDic=controlStructure["system"][sys]
    currentDic=updateUsingEstimatedTime(items,currentDic,timeElapsed_tosend,sys)
    currentDic=updateAllProbas(items,currentDic,sys,c,meta_coef)
    controlStructure["system"][sys]=currentDic
    return controlStructure

def updateAllProbas(items,currentDic,sys,c,meta_coef):
    for currentImage in list(set(sys)):
        currentDic[currentImage]=computeProbabilityVector(currentDic[currentImage],c,meta_coef)
    return currentDic

def updateUsingEstimatedTime(items,currentDic,totalRT,sys):
    # estimated time for each item is totalRT minus the sum of the others item (based on previous perfs)
    for i,item in enumerate(items):
        sumItem=0
        currentImage=sys[i]
        for j,item2 in enumerate(items):
            if(item2!=item):
                currentImage2=sys[j]
                sumItem+=currentDic[currentImage2]["rtItems"][item2][-1] # last value is the most precise
        currentDic[currentImage]=updateRTmeanVector(currentDic[currentImage],item,totalRT-sumItem)
    return currentDic
                
    
def computeProbabilityVector(dic,c=1.0352649,meta_c=1):
    d={}
    for index,listRT in dic["rtItems"].iteritems():
        d[index]=listRT[-1]
    number_items=len(d)
    sorted_x = sorted(d.items(), key=operator.itemgetter(1))
    coeff=1
    sumrt=0
    c=((c-1)/math.pow(meta_c, number_items))+1 
    # the attenuation coefficient at start for easy items
    # will be multiplied by meta_c at each step, so must be initialized
    # with this line to reach, at the last item, the attenuation (c) given 
    dic["probas"]={}
    for t in sorted_x:
        dic["probas"][t[0]]=coeff
        sumrt+=coeff
        coeff*=c
        c=(c-1)*meta_c+1
        # the 20th first elements got 50% chance, 20-40 : 25% etc....
        # if one item are 20 spot later, it has twice less probability to occur
    for index2,dicRt2 in dic["probas"].iteritems():
        dic["probas"][index2]=dic["probas"][index2]/sumrt
    return dic

def updateRTmeanVector(dic=None,item=None,rtVal=None):
    vals=dic["rtItems"][item]
    newVal=float(sum(vals)+rtVal)/(len(vals)+1)
    dic["rtItems"][item].append(newVal)
    dic["rtItems"][item].pop(0)
    return dic

def createRtDic(items,memSize, defaultTime=1):
    dic={}
    dic["rtItems"]={}
    dic["probas"]={}
    for item in items:
        dic["probas"][item]=1/float(len(items))
        dic["rtItems"][item]={}
        dic["rtItems"][item]=[]
        for i in range(memSize):
            dic["rtItems"][item].append(defaultTime) 
    return dic


def createString(number,mode):
    if (mode=="n")and(int(number)<10):
        return ('0'+str(number))
    return str(number)

def findType(system,indexItem):
    i=indexItem%len(system)
    return system[i]

def printSumStruc(controlStructure,selectedSystem):
    message=""
    for d,dic in controlStructure["system"][selectedSystem['system']].iteritems():
        prefix="values for "+d+"\n"
        message=printSumDic(dic,prefix,message)
    writeLongMessageInFile(message)
        

def printSumDic(dic,prefix="",message=""):
    d={}
    for index,dicRt in dic["rtItems"].iteritems():
        d[index]=dicRt[-1] # Last element
    sorted_x = sorted(d.items(), key=operator.itemgetter(1))
    it = iter(sorted_x)
    message+="\n"+prefix+"order list of reaction times based on few last trials"
    for val in it:
        message+="\n %s : %.2f"%(val[0],float(val[1]))
    return message

def buildAStructure(dicSys,selectedSystem,mode="d"):
    # still only working for numbers
    if(dicSys==None):
        dicSys={}        
    sys=selectedSystem["system"]
    if("system" not in dicSys):
        dicSys["system"]={}
    dicSys["system"][sys]={}
    components=list(set(sys))
    d={}
    for component in components:
        size=int(selectedSystem["imagesSize"][component])
        items=createRandomList(mode,size)
        d[component]=createRtDic(items,4)
    dicSys["system"][sys]=d
    if ("infos" not in dicSys):
        dicSys["infos"]={"compteur":0}   
    return dicSys
    
def displayItemForTrainingRT(lastIt, controlStructure,selectedSystem,nbDigits,separator="|",mode="d"):
    currentDic=controlStructure["system"][selectedSystem["system"]]
    items,lastIt = takeItems(currentDic,lastIt,selectedSystem["system"],mode)
    if(mode=="d"): # very bad practice as this function does not print for other feats than numbers
        message=separator.join(items)
        printNumber(message) 
    return items,lastIt
    
def createRandomList(mode="d",n=2):
    v=[]
    if mode=="d":
        v = [turnIntoPrintableString(str(x),n) for x in range(0,pow(10,n))]
    if mode=="b":
        v=[str(x) for x in itertools.product([0, 1], repeat=6)]
    if mode=="mb":
        v=[str(x) for x in itertools.product([0, 1], repeat=3)]
    if mode=="c":
        v=[card+suit for suit in ("C","H","S","D") for card in ("2","3","4","5","6","7","8","9","T","J","Q","K","A")]
    rd.shuffle(v)
    return v
