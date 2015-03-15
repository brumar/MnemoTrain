import random
import time
import os
import msvcrt
import csv

nbRows=20
lengthColumn=40
indent=5
maxTime=300
restiTime=900


sepN=raw_input("separaters every N digits (default=2) : ")
nr=raw_input("how many rows (default=20) : ")
mt=raw_input("how much time (s) (default=300s) : ")
rt=raw_input("how much time to write (s) (default=900s) : ")

if (mt!=""):
    maxTime=float(mt)

if (rt!=""):
    restiTime=float(rt)
    
if (nr!=""):
    nbRows=int(nr)
    
if(sepN==""):
    sepN=2
else:
    sepN=int(sepN)

                
def print_debrief(table,errors,points,nl):
    print_table(table,nl)
    print("\n")
    print("you got "+str(points)+" points")
    for error in errors:
        print "at line %d,column %d you wrote %s, instead of %s"  % (error[0], error[1],error[2],error[3])
                
def print_table(table,nL=nbRows):
    print("\n"*(10+(20-nL)/2))
    lines=table.splitlines()
    for l in range(nL):
        print(lines[l])

def raw_input_with_timeout(prompt, timeout=30.0):
    print prompt,    
    finishat = time.time() + timeout
    result = []
    while True:
        if msvcrt.kbhit():
            result.append(msvcrt.getche())
            if (result[-1] == 'q')or(result[-1] == 'v'):   # or \n, whatever Win returns;-)
                return ''.join(result)
            time.sleep(0.1)          # just to yield to other processes/threads
        else:
            if time.time() > finishat:
                return None
    
def buildAnswerFromFile(fname):
    answer=[]
    with open(fname, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            lanswer=[]
            for element in row:
                lanswer.extend(element)
            answer.append(lanswer)
    return answer

def compareSolutionAnswer(lsol,lansw):
    indexL=0
    points=0
    errors=[]
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
            

table=""
solution=[]
for r in range(nbRows):
    solutionline=[]
    row=" "*indent
    for l in range(lengthColumn):
        sep=""
        if(l%sepN==0):
            sep="|"       
        d=random.randint(0, 9)
        solutionline.append(str(d))
        row+=sep+str(d)
    table+=row+"|"+"\n"
    solution.append(solutionline)
print_table(table)
print("\n"*9)
time.sleep(maxTime)
print("\n"*30)
with open('temp.txt', 'w') as f:
    pass
os.system("start "+"temp.txt")# windows only, for mac : os.system("open "+filename)
#raw_input_with_timeout("quit (q), load the answer file(l)",10)
do=raw_input("quit (q), load the answer file(l) : ")
if(do=="l"):
    answer=buildAnswerFromFile("temp.txt")
    [errors,points,nlines]=compareSolutionAnswer(solution,answer)
    print_debrief(table,errors,points,nlines)
