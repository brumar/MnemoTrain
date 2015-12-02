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

    
def computeProbabilityVector(dic,c=1.0352649,meta_c=1):
    d={}
    for index,dicRt in dic.iteritems():
        if(index!="probas"):
            d[index]=dicRt[2]
    #print(d)
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
    vals=dic[item]
    newVal=0.25*vals[0]+0.25*vals[1]+0.25*vals[2]+0.25*rtVal
    vals[0]=vals[1]
    vals[1]=vals[2]
    vals[2]=newVal
    dic[item]=vals
    return dic

def convertDic(initDic):
    dic={}
    dic["probas"]={}
    for i,rt in initDic.iteritems():
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

def  printSumDic(dic):
    d={}
    for index,dicRt in dic.iteritems():
        if(index!="probas"):
            d[index]=dicRt[2]
    #print(d)
    sorted_x = sorted(d.items(), key=operator.itemgetter(1))
    it = iter(sorted_x)
    print("order list of reaction times based on last 4 trials")
    for val in it:
        print("%s : %.2f "%(val[0],float(val[1])))


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
