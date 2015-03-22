from random import random
import operator
import time
import pickle
#TODO: store and retrieve previous datas
initDic={}
f1=open('./rawDatas/numbersLoop.csv', 'a')

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

def takeItem(vec):
    r=random()
    i=0
    cumul=0
    while True:
        cumul+=vec[i]
        if(r<cumul):
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

if __name__ == "__main__":
    system = raw_input('images to train PAP, PA, P or A) : ')
    if(system==''):
        system="PA"
    coef=raw_input("attenuation coefficient in % (default : 3.5) : ")
    c=1.0352649
    if (coef!=""):
        c=1+float(coef)/100

    timeP=raw_input("how much practice in minutes (default : 3) : ")
    t=180
    if (timeP!=""):
        t=float(timeP)*60

    #initDic={"00":0.856974449094,"01":0.954354421038,"02":1.14549382512,"03":0.972335362472,"04":0.865442435003,"05":0.845586146315,"06":1.166294785,"07":1.08075935703,"08":1.10255490406,"09":0.857419494188,"10":0.855345416105,"11":0.985545831014,"12":0.770835364571,"13":0.958828197199,"14":0.842853830677,"15":0.83752075361,"16":1.12890773152,"17":0.928795117379,"18":0.954391274877,"19":0.83961955642,"20":0.884804229141,"21":1.74740658601,"22":1.00925031361,"23":0.979187377514,"24":0.963826790688,"25":1.05470649183,"26":0.886336229236,"27":1.10784786175,"28":1.11975491731,"29":0.744676136393,"30":1.12951605311,"31":0.87704253073,"32":1.05017580214,"33":0.861780842815,"34":0.95555893512,"35":0.869979655748,"36":0.849511313429,"37":0.901413647956,"38":1.46334045996,"39":1.1316890301,"40":1.10228153254,"41":0.830396300061,"42":1.04315351303,"43":0.909781801947,"44":1.00760681899,"45":0.938952315331,"46":1.09702169665,"47":0.980794951304,"48":1.06631964967,"49":1.03062787279,"50":0.939073139943,"51":1.02360931572,"52":1.01562416175,"53":0.941010998772,"54":1.05097679001,"55":0.755317565799,"56":0.89105585316,"57":2.01201201902,"58":0.946855831047,"59":0.864223925792,"60":1.00444298688,"61":0.979365582153,"62":1.05567402173,"63":1.09192840279,"64":0.85822188157,"65":0.868326831041,"66":1.00938746587,"67":1.13008098981,"68":1.06426096623,"69":0.938264688004,"70":1.0561708488,"71":0.843573180295,"72":0.845546959955,"73":1.10504930251,"74":1.0088257947,"75":1.01324452336,"76":1.02180767614,"77":0.927769740945,"78":1.02776540246,"79":1.00344466769,"80":1.12976143437,"81":1.06782505902,"82":1.04683936345,"83":1.11403650769,"84":1.08585638292,"85":0.965271087977,"86":1.04934729052,"87":1.04617879337,"88":0.857334590407,"89":0.998478729504,"90":1.05510768552,"91":0.880616420111,"92":1.06581069349,"93":0.950248716763,"94":1.00918267049,"95":1.04328413424,"96":0.928264702,"97":0.908065066153,"98":0.945126966141,"99":1.13270460995}
    [dic,vec] = pickle.load( open( "saveRt.p", "rb" ) )
    dic=convertDic(initDic)
    vec=computeProbabilityVector(dic)
    ok=True
    trials=0
    waiter()
    startExp= time.clock()
    while(True):
        startTrial= time.clock()
        trials+=1
        item=takeItem(vec)
        sitem=str(item)
        printNumber("0"*(2-len(sitem))+sitem)
        Userinput=raw_input("")
        nt=time.clock()
        if (Userinput=="q")or((nt-startExp)>t):
            datas=[]
            datas.extend([vec,dic])
            pickle.dump( datas, open( "saveRt.p", "wb" ) )
            break
        timeElapsed=nt-startTrial
        if(timeElapsed>4):
            timeElapsed=2
        if(timeElapsed<0.4):
            timeElapsed=1
        dic=updateRTmeanVector(dic,item,timeElapsed)
        vec=computeProbabilityVector(dic,c)
        f1.write(str(trials)+";"+str(c)+";"+str(item)+";"+str(t)+";"+system+";"+ str(time.time())+ ";"+str(timeElapsed)+";numbers\n")


