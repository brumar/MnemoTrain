import time
import random as rd
import itertools
import operator

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

def takeItem(vec,lastIt):
    while True:# loop related to last Item checking
        r=rd.random()
        i=0
        cumul=0
        while True:
            cumul+=vec[i]
            if(r<cumul):
                if(not lastIt.contains(i)):
                    return i
            i+=1


def computeProbabilityVector(dic,c=1.0352649):
    d={}
    for index,dicRt in dic.iteritems():
        d[index]=dicRt[2]
    #print(d)
    sorted_x = sorted(d.items(), key=operator.itemgetter(1))
    coeff=1
    d2={}
    sumrt=0
    for t in sorted_x:
        d2[t[0]]=coeff
        sumrt+=coeff
        coeff*=c
        # the 20th first elements got 50% chance, 20-40 : 25% etc....
        # if one item are 20 spot later, it has twice less probability to occur
    v=[]
    for i in range(100):
        v.append(d2[i])
    #print(d2,v)
    vec = [x / sumrt for x in v]
    return vec

def updateRTmeanVector(dic=None,item=None,rtVal=None):
    #print(dic)
    if(dic==None):
        dic={}
        for i in range(100):
            dic[i]={}
            dic[i][0]=1
            dic[i][1]=1
            dic[i][2]=1
    else:
        vals=dic[item]
        newVal=0.25*vals[0]+0.25*vals[1]+0.25*vals[2]+0.25*rtVal
        vals[0]=vals[1]
        vals[1]=vals[2]
        vals[2]=newVal
        dic[item]=vals
    return dic

def convertDic(initDic):
    dic={}
    for k,rt in initDic.iteritems():
        i=int(k)
        dic[i]={}
        dic[i][0]=rt
        dic[i][1]=rt
        dic[i][2]=rt
    return dic


def createString(number,mode):
    if (mode=="n")and(int(number)<10):
        return ('0'+str(number))
    return str(number)

def findType(system,indexItem):
    i=indexItem%len(system)
    return system[i]



def createRandomList(n,mode): # n probably useless
    v=[]
    if mode=="n":
        v = [x for x in range(0,100)]
    if mode=="b":
        v=[bits for bits in itertools.product([0, 1], repeat=6)]
    if mode=="mb":
        v=[bits for bits in itertools.product([0, 1], repeat=3)]
    rd.shuffle(v)
    return v[:n]