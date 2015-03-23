#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mnemy.disciplines import Binaries, Words, Numbers, Dates, profileLoader, errorsLoader, reportDatas,lociLoader
from mnemy.utils import smartRawInput
import time

if __name__ == "__main__":

    #===========================================================================
    # Load Discipline Parameters
    #===========================================================================

    feat=raw_input("pick your feat (d=digits,b=binaries,w=words,h=historicalDates) : ")
    if(feat=="")or(feat=="d"):
        feat="d"
        sep,row,col,memoTime,restiTime,sepSign=2,20,40,300,900,"|"

    if(feat=="h"):
        sep,row,col,memoTime,restiTime,sepSign=1,60,1,300,900,"|"

    if(feat=="w"):
        freqMax=smartRawInput("N Most frequent words",8000,int)
        sep,row,col,memoTime,restiTime,sepSign=1,20,5,300,900,"|"

    if(feat=="b"):
        sep,row,col,memoTime,restiTime,sepSign=6,25,30,300,900,"|"

    else:
        sep=smartRawInput("separaters every N items",sep,int)

    row=smartRawInput("how many rows",row,int)
    col=smartRawInput("how many cols",col,int)
    memoTime=smartRawInput("how much time to learn (s)",memoTime,float)
    restiTime=smartRawInput("how much time to write (s)",restiTime,float)

    memoTime=2    #commented line for debugging purpose

    #===========================================================================
    # Proceed to the discipline
    #===========================================================================

    if(feat=="b"):
        ff=Binaries(row, col,memoTime,restiTime,sepSign,sep,"bin_temp.txt",indent=5)
    if(feat=="w"):
        ff=Words(row, col,memoTime,restiTime,sepSign,sep,"word_temp.txt",indent=2,freqMax=freqMax,sizeCell=20)
    if(feat=="d"):
        ff=Numbers(row, col,memoTime,restiTime,sepSign,sep,"num_temp.txt",indent=5)
    if(feat=="h"):
        ff=Dates(row, col,memoTime,restiTime,sepSign,sep,"dates_temp.txt",indent=5)
    [solution,answer,attempt]=ff.proceed()

    #===========================================================================
    # Report the results
    #===========================================================================

    report=raw_input("report results (y/n) (default=y) : ")

    if(report!="n"):
        pr=raw_input("load profile (y/n) (default=y) : ")
        locis,systemDic,errorsDic=None,None,None
        if(pr!="n"):
            systemDic=profileLoader('profile.properties',feat,row,col)
        ed=raw_input("load errors Dic (y/n) (default=y) : ")
        if(ed!="n"):
            errorsDic=errorsLoader('errors.properties')
        lo=raw_input("load journey (y/n) (default=y) : ")
        checker="n"
        if(lo!="n"):
            locis=lociLoader()
            checker=raw_input("proceed to loci checker (advised) (y/n) (default=y) : ")
            if(checker==""):
                checker="y"
        if(systemDic!=None):
            globalReport=[attempt,feat,str(row), str(col),str(memoTime),str(restiTime),sepSign,str(round(time.time()))]
            reportDatas(solution,answer,systemDic,errorsDic,globalReport,locis,checker,ff.revert)


