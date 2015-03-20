#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import os
import msvcrt
import csv
from os import listdir
from os.path import isfile, join
from feats import *
import uuid

#TODO

#custom user error repot (writing error)
#go directly to restitution
#pouvoir abandonner le chargement des locis
#voir les index des locis

locipath="./Loci"
datas="./rawDatas/feats.csv"
f2=open('./rawDatas/global.txt', 'a') #print globalMessages

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
    lastLoci=["",""]
    #if loci is not defined, default values avoiding bugs
    if(locis==None):
        indexLoci=""
        currentLoci=["",""]
    while cont:
        for b,bloc in enumerate(blocs):
            if(locis!=None):
                #print(locis)
                #print(indexLoci)
                try:
                    currentLoci=locis[indexLoci]
                except IndexError:
                    decision=raw_input("your journey seems too short for this feat. This also may be dued to incorrect profile settings.\n reload another journey(r), use blank locis(b), quit(q) : ")
                    if(decision=="r"):
                        raw_input("fix your loci csv files by adding or deleting locis, eventually with a csv temp file (must keep the loci id though) then push enter")
                        locis=lociLoader()
                        reportDatas(sol,ans,system,globalReport,locis,checker="y")
                    if(decision=="q"):
                        os._exit(1)
                    else:
                        currentLoci=["",""]
                        locis=None
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
                lastLoci=currentLoci
                #print(answer,sol,currentLoci)
                indexAns+=size
    if(checker=="y")and(locis!=None):
        checked=raw_input("the last loci you used was %s, containing %s, right ? (y/n) : "%(lastLoci[1],solution))#lastLoci = Trick to avoid strange bug
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
    message+="\n choice : "
    il=raw_input(message)
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


def profileLoader(profileFile):
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

if __name__ == "__main__":

    feat=raw_input("pick your feat (d=digits,b=binaries,w=words,h=historicalDates) : ")
    if(feat=="")or(feat=="d"):
        feat="d"
        sep,row,col,memoTime,restiTime,sepSign=2,20,40,300,900,"|"

    if(feat=="h"):
        sep,row,col,memoTime,restiTime,sepSign=1,60,1,300,900,"|"

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

    if (mt!=""): memoTime=float(mt)
    if (rt!=""): restiTime=float(rt)
    if (nr!=""): row=int(nr)
    if (nc!=""): col=int(nc)
    if (sepN!=""): sep=int(sepN)

    memoTime=2    #commented line for debugging purpose
    #sep,row,col,memoTime,restiTime,sepSign=2,40,20,300,900
    if(feat=="b"):
        ff=Binaries(row, col,memoTime,restiTime,sepSign,sep,"bin_temp.txt",indent=5)
    if(feat=="w"):
        ff=Words(row, col,memoTime,restiTime,sepSign,sep,"word_temp.txt",indent=2,freqMax=freqMax,sizeCell=20)
    if(feat=="d"):
        ff=Numbers(row, col,memoTime,restiTime,sepSign,sep,"num_temp.txt",indent=5)
    if(feat=="h"):
        ff=Dates(row, col,memoTime,restiTime,sepSign,sep,"dates_temp.txt",indent=5)
    [solution,answer,attempt]=ff.proceed()
    report=raw_input("report results (y/n) (default=n) : ")

    if(report=="y"):
        pr=raw_input("load profile (y/n) (default=n) : ")
        locis,systemDic=None,None
        if(pr=="y"):
            systemDic=profileLoader('profile.properties')
        lo=raw_input("load journey (y/n) (default=n) : ")
        checker="n"
        if(lo=="y"):
            locis=lociLoader()
            checker=raw_input("proceed to loci checker (advised) (y/n) (default=y) : ")
            if(checker==""):
                checker="y"
        if(systemDic!=None):
            globalReport=[attempt,feat,str(row), str(col),str(memoTime),str(restiTime),sepSign,str(round(time.time()))]
            reportDatas(solution,answer,systemDic,globalReport,locis,checker,ff.revert)


