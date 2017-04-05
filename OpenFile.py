import json,os
from pprint import pprint

# To read the data file
print os.getcwd()
with open('../Task 4/Restaurants_Train.xml.term-polarity.json') as FH:
    SentsDict = json.load (FH)

Lines = []
for Id, SentStruct in SentsDict.iteritems():
    Sent = SentStruct['Sentence']
    for Index,Term in enumerate(SentStruct['TermAndPolarity']['Term']):
        Pol = SentStruct['TermAndPolarity']['Polarity'][Index]
        Tup = (Sent,Term,Pol) # list structure
        Lines.append ('; '.join(Tup))

OPFName = 'RestAspTermABSA.data'
with open (OPFName,'w') as FH:
    for L in Lines:
        print >>FH, L