import random

dictionnary='./dictionnaries/french/newDic.csv'
nbRows=20
lengthColumn=5

verbs=[]
nouns=[]

#time=raw_input("length in minutes (default 5)")
sizecell=20


with open(dictionnary, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        if(row[0]=="n"):
            nouns.append(row[1])
        if(row[0]=="v"):
            verbs.append(row[1])

table=""
for r in range(nbRows):
    row=""
    for l in range(lengthColumn):
        word=""
        if(random.randint(0, 9)==9):
            word=random.choice(verbs)
        else:
            word=random.choice(nouns)
        decalTotal=sizecell-len(word)
        decalLeft=decalTotal/2
        decalRight=decalTotal-decalLeft
        row+=" "*decalLeft+word+" "*decalRight+"|"
    table+=row+"\n"

print(table)


