import random

dictionnary='./dictionnaries/french/newDic2.csv'
nbRows=20
lengthColumn=5

verbs=[]
nouns=[]

number_input=raw_input("N th Most frequent words (no if no limit, default=8000) : ")
if(number_input==""):
    number_input=8000
else:
    if(number_input=="no"):
        number_input=100000
    else:
        number_input=float(number_input)

sizecell=20


with open(dictionnary, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for r,row in enumerate(spamreader):
        if(r==number_input):
            break
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


