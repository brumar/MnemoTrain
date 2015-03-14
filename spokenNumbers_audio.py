import time
import random
import winsound, sys

n = raw_input('numbers (100 by default) : ')
f = raw_input('freq (1s by default) : ')

def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)

    
if(n==""):
    n=25
else:
    n=int(n)

if (f==""):
    f=1.0
else:
    f=float(f)

t0= time.clock()

for x in range(0,n):
    while True:
        nt=time.clock()
        if(nt - t0>f):
            print(t0)
            print(nt - t0)
            t0=nt
            break        
    m=str(random.randint(0, 9))
    print(m)
    sound=m
    beep(sound)




