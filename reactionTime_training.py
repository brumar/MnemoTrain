from mnemy.training import *

# still dirty but not usefull enough to get pimped up

if __name__ == "__main__":
    n = 1000

    mode = raw_input('what do you want to train (b/mb/n), default = n : ')
    system = raw_input('system (PAP)(P)(A) : ')
    f2=open('./rawDatas/global.txt', 'a')
    filename="numbers.csv" # by default

    if (mode==""):
        mode="n"

    if mode=="mb":
        filename="minibinaries.csv"
        goal= raw_input('goal (6s by default) :  ')

    else:
        if mode=="b":
            filename="binaries.csv"
            goal= raw_input('goal (3s by default) :  ')
        else :
            goal= raw_input('goal (1.15s by default) :  ')
        scoreLimit = raw_input('how many items below your bar ? (default 30)   ')


    f1=open('./rawDatas/'+filename, 'a')

    if (scoreLimit==""):
        scoreLimit=30
    else:
        scoreLimit=int(scoreLimit)

    if (system==""):
        system="P"

    if (goal==""):
        if(mode=="mb"):
            goal=6
        else:
            if (mode=="b"):
                goal=3
            else:
                goal=1.15
    else:
        goal=float(goal)

    t0= time.clock()
    randomList=createRandomList(n,mode)
    limit=len(randomList)
    score=0
    tstartExperiment= time.clock()
    waiter()
    print "\n" * 50
    trials=0

    if (mode=="mb"):
        ok=True
        while(ok):
            trials+=1
            tstartExperiment= time.clock()
            ts=tstartExperiment
            randomList=createRandomList(n,mode)
            for i,m in enumerate(randomList):
                ms=createString(m,mode)
                printNumber(ms)
                Userinput=raw_input("")
                if (Userinput=="q"):
                    ok=False
                    break
            timeElapsed=time.clock()-ts
            f1.write(system+";"+findType(system,i)+";"+ str(i)+";"+ str(time.time())+ ";"+str(timeElapsed)+";miniBinaries\n")
            if(timeElapsed<goal):
                print("you accomplished your goal (<"+str(goal)+" s)"+" in "+str(trials)+" trials ")
                ok=False
                break
            else:
                ts=time.clock()

    else:
        for i,m in enumerate(randomList):
            if(score==scoreLimit):
                message="you got your goal (<"+str(goal)+" s)"+"for "+str(int(scoreLimit))+" items ("+str(i)+" total items viewed) in "+str(int(time.clock()-tstartExperiment))+" seconds "+"\n"
                print(message)
                f2.write(message)
                break
            ms=createString(m,mode)
            tstart= time.clock()
            printNumber(ms)
            Userinput=raw_input("")
            #print "\n" * 20
            if (Userinput=="q"):
                f1.close()
                break
            else :
                tfinal= time.clock()
                timeElapsed=tfinal-tstart
                if(timeElapsed>goal):
                    decalage=random.randint(3,6)
                    if(i+decalage<limit):
                        randomList.insert(i+decalage,m)
                else:
                    score+=1
                f1.write(system+";"+findType(system,i)+";"+ str(i)+";"+ str(time.time())+ ";"+str(timeElapsed)+";"+ms+"\n")
    f1.close()
    f2.close()



