import pickle
import stanza
import os
import pickle

def getNegAndPosWords():
    with open("dicts/annotated.dict") as dictFile:
        lines = iter(dictFile.readlines())
        negativeWords = {}
        positiveWords = {}
        next(lines)
        c = 2
        try:
            while ((neg := next(lines).strip()) != "POSITIVE"):
                neg = neg.split("(")
                neg[0] = neg[0].strip()
                neg[1] = neg[1].replace(")", "")
                neg[1] = float(neg[1])
                negativeWords[neg[0]] = neg[1]
                c += 1
                
        
            while True:
                try:
                    pos = next(lines).strip()
                    c += 1
                    pos = pos.split("(")
                    pos[0] = pos[0].strip() 
                    pos[1] = pos[1].replace(")","")
                    pos[1] = float(pos[1])           
                    positiveWords[pos[0]] = pos[1]
                except StopIteration:
                    break
        except Exception as e:
            print(e)
            print("line %d"%c)
    dictFile.close()

    return (positiveWords, negativeWords)


def openTweets():
    with open("exemple_datasets/bonheur.lst") as bonheurFile:
       bonheurTweets = pickle.load(bonheurFile)
       bonheurFile.close()
    with open("exemple_datasets/haine.lst") as haineFile:
       haineTweets = pickle.load(haineFile)
       haineFile.close()
    
    return (haineTweets, bonheurTweets)


nlp = stanza.Pipeline(lang='fr', processors='tokenize', dir=os.getenv("DATA_DIR"))


f = open("exemple_datasets/haine.lst", "rb")
haineTweets = pickle.load(f)
f.close()

f = open("exemple_datasets/bonheur.lst", "rb")
bonheurTweets = pickle.load(f)
f.close()

posWords, negWords = getNegAndPosWords()

hatescore = 0

for tweet in haineTweets:
    doc = nlp(tweet["text"])
    for sentence in doc.sentences:
        for word in sentence.words:
            if (word.text.upper() in negWords):
                hatescore -= negWords[word.text.upper()]
            if (word.text.upper() in posWords):
                hatescore += posWords[word.text.upper()]

print("hate tweets score : %f"%hatescore)

happyscore = 0

for tweet in bonheurTweets:
    doc = nlp(tweet["text"])
    for sentence in doc.sentences:
        for word in sentence.words:
            if (word.text.upper() in negWords):
                happyscore -= negWords[word.text.upper()]
            if (word.text.upper() in posWords):
                happyscore += posWords[word.text.upper()]

print("happiness tweets score : %f"%happyscore)



