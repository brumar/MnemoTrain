import sys
import random
import winsound, sys
import os
import time

n = raw_input('numbers (15 by default) : ')
system = raw_input('system (PAP)(P)(A) : ')
f1=open('./times.txt', 'a')


def createString(number):
    if (int(number)<10):
        return ('0'+str(number))
    return str(number)

def findType(system,indexItem):
    i=indexItem%len(system)
    return system[i]

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

    
if(n==""):
    n=25
else:
    n=int(n)

if (system==""):
    system="PAP"

t0= time.clock()
waiter()
print "\n" * 50
for i in range(0,n):        
    m=str(random.randint(0, 99))
    ms=createString(m)
    tstart= time.clock()
    printNumber(ms)
    Userinput=raw_input("")
    print "\n" * 20
    if (Userinput=="q"):
        f1.close()
        break
    else :
        tfinal= time.clock()
        timeElapsed=tfinal-tstart
        f1.write(system+";"+findType(system,i)+";"+ str(i)+";"+ str(time.time())+ ";"+str(timeElapsed)+";"+ms+"\n")
f1.close()




