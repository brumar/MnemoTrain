#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mnemy.disciplines import Binaries, Words, Numbers, SpokenNumbers, Dates, profileLoader, errorsLoader, reportDatas,loadAndCheckJourney, Cards, AbstractImages,NameAndFaces
from mnemy.utils import smartRawInput

import time

#    TODO : avoid permission denied error by looping

if __name__ == "__main__":
    while True:
        training=smartRawInput("Special training(s) or test yourself(t)","s")
        if(training=="s"):
            train=raw_input("pick your discipline (d=digits,c=Cards,k=spokenNumber) : ")
            if(train=="k"):
                ff=SpokenNumbers()
            elif(train=="d"):
                ff=Numbers()
            elif(train=="c"):
                ff=Cards()
            else:
                raise Exception("sorry no training game for this feat")

            ff.trainingGame()
        else:
            #===========================================================================
            # Load Discipline Parameters
            #===========================================================================

            feat=raw_input("pick your discipline (d=digits,b=binaries,w=words,h=historicalDates,s=SpeedCards,c=Cards,a=AbstractImages,n=NameAndFaces) : ")

            #===========================================================================
            # Set defaults values
            #===========================================================================

            if(feat=="")or(feat=="d"):
                feat="d"
                sep,row,col,memoTime,restiTime,sepSign,uniBloc=2,20,40,300,900,"|",False

            if(feat=="h"):
                sep,row,col,memoTime,restiTime,sepSign,uniBloc=1,60,1,300,900,"|",True

            if(feat=="w"):
                freqMax=smartRawInput("N Most frequent words",8000,int)
                sep,row,col,memoTime,restiTime,sepSign,uniBloc=1,20,5,300,900,"|",True

            if(feat=="b"):
                sep,row,col,memoTime,restiTime,sepSign,uniBloc=6,25,30,300,900,"|",False

            if(feat=="s"):
                row,col,sep,memoTime,restiTime,sepSign,uniBloc=1,52,3,300,900,"|",False

            if(feat=="c"):
                row,col,sep,memoTime,restiTime,sepSign,uniBloc=2,52,3,600,1200,"|",False

            if(feat=="a"):
                sep,row,col,memoTime,restiTime,sepSign,uniBloc=1,2,5,300,900,"|",True

            if(feat=="n"):
                sep,row,col,memoTime,restiTime,sepSign,uniBloc=1,2,5,300,900,"|",True
                freqMax=smartRawInput("N Most frequent names",5000,int)
            #===========================================================================
            # Override default values
            #===========================================================================

            if(feat not in ["s","c"]):
                row=smartRawInput("how many rows",row,int)
                col=smartRawInput("how many cols",col,int)
                sep=smartRawInput("separation every N items",sep,int)
            else:
                sep=smartRawInput("number cards to display each time",sep,int)
            memoTime=smartRawInput("how much time to learn (s)",memoTime,float)
            restiTime=smartRawInput("how much time to write (s)",restiTime,float)



            #memoTime=2    #commented line for debugging purpose

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
            if(feat =="c"): #MUST BE SIMPLIFIED
                ff=Cards(row, col,memoTime,restiTime,sep,"cards_temp.txt",manyDecks=True)
            if(feat =="s"): #MUST BE SIMPLIFIED
                ff=Cards(row, col,memoTime,restiTime,sep,"cards_temp.txt",manyDecks=False)
            if(feat =="a"):
                ff=AbstractImages(row, col,memoTime,restiTime)
            if(feat =="n"):
                ff=NameAndFaces(row, col,memoTime,restiTime)
            [solution,answer,attempt]=ff.proceed()

            #===========================================================================
            # Report the results
            #===========================================================================

            report=raw_input("report results (y/n) (default=y) : ")

            if(report!="n"):
                pr=raw_input("load profile (y/n) (default=y) : ")
                locis,systemDic,errorsDic=None,None,None
                if(pr!="n"):
                    systemDic=profileLoader('user/profile.properties',feat,row,col)
                ed=raw_input("load errors Dic (y/n) (default=y) : ")
                if(ed!="n"):
                    errorsDic=errorsLoader('user/errors.properties')
                lo=raw_input("load journey (y/n) (default=y) : ")
                if(lo!="n"):
                    locis=loadAndCheckJourney(systemDic,answer)
                globalReport=[attempt,feat,str(row), str(col),str(memoTime),str(restiTime),sepSign,str(round(time.time()))]
                reportDatas(solution,answer,systemDic,errorsDic,globalReport,locis,ff.revert)
        choice=smartRawInput("quit(y/n)","n",str)
        if (choice=="y"):
            break


