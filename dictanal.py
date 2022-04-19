import pickle
import stanza
import os
import pickle

def getNegAndPosWords():
    with open("dicts/frlsd.cat") as dictFile:
        lines = iter(dictFile.readlines())
        negativeWords = []
        positiveWords = []

        next(lines)
        while ((neg := next(lines).strip()) != "POSITIVE"):
            neg = neg.split("(")
            neg[0] = neg[0].strip()
            neg[1] = neg[1].replace(")", "")
            neg[1] = int(neg[1])
            negativeWords.append(neg)
    
        while True:
            try:
                pos = next(lines).strip()
                pos = pos.split("(")
                pos[0] = pos[0].strip() 
                pos[1] = pos[1].replace(")","")
                pos[1] = int(pos[1])           
                positiveWords.append(pos)
                print(pos)
            except StopIteration:
                break
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

nlp = stanza.Pipeline(lang='fr', processors='tokenize,sentiment', dir=os.getenv("DATA_DIR"))


posWords, negWords = getNegAndPosWords()

score = 0

for tweet in haineTweets:
    doc = nlp(tweet["text"])
    for word in doc.sentences:
        if (word in negWords):
            score -= 1
        if (word in posWords):
            score += 1
