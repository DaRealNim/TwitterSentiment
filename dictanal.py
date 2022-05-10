import pickle
import stanza
import os
import pickle
import string

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
    with open("exemple_datasets/bonheur.lst", "rb") as bonheurFile:
       bonheurTweets = pickle.load(bonheurFile)
       bonheurFile.close()
    with open("exemple_datasets/haine.lst", "rb") as haineFile:
       haineTweets = pickle.load(haineFile)
       haineFile.close()
    with open("exemple_datasets/ironique.lst", "rb") as ironieFile:
       ironieTweets = pickle.load(ironieFile)
    
    return (haineTweets, bonheurTweets, ironieTweets)

def process_word(word):
    for symbol in string.punctuation:
        word.replace(symbol, "")
    return word.upper()

def sentence_contains_ironic_adjective(words:list) -> bool:
    for index in range(1, len(words) - 1):
        preword, word, nextword = words[index-1], words[index], words[index+1]
        print(f"{preword.text} {word.text} ({word.upos}) {nextword.text}")
        if preword.text == "\"" and nextword.text == "\"" and word.upos == "ADJ":
              return True
    return False

def process_sentence(stz_sentence, posWords, negWords):
    sentence_score = 0
    irony = sentence_contains_ironic_adjective(stz_sentence.words)
    for stz_word in stz_sentence.words:
        w = process_word(stz_word.text)
        for negword in negWords:
            if negword == w or (negword.endswith("*") and w.startswith(negword[:-1])):
                sentence_score -= negWords[negword]
                break
        for posword in posWords:
            if posword == w or (posword.endswith("*") and w.startswith(posword[:-1])):
                sentence_score += posWords[posword]
                break
    if irony:
        return sentence_score * -1
    return sentence_score

def process_tweet(nlp, tweet, posWords, negWords):
    doc = nlp(tweet["text"])
    tweet_score = 0
    for sentence in doc.sentences:
        tweet_score += process_sentence(sentence, posWords, negWords)
    # very basic irony detection
    if tweet["text"].endswith("/s"):
        tweet_score *= -1
        print("Ironic tweet: " + tweet["text"])
    return tweet_score


if __name__ == "__main__":
    nlp = stanza.Pipeline(lang='fr', processors='tokenize, pos', dir=os.getenv("DATA_DIR"))

    print("\n\n=======================\n")
    posWords, negWords = getNegAndPosWords()
    haineTweets, bonheurTweets, ironieTweets = openTweets()

    # handle irony
    for tweet in ironieTweets:
        print(tweet["text"] + " : " + str(process_tweet(nlp, tweet, posWords, negWords)))


    hatescore = 0
    for tweet in haineTweets:
        hatescore += process_tweet(nlp, tweet, posWords, negWords)
    print("hate tweets score : %f"%hatescore)

    happyscore = 0
    for tweet in bonheurTweets:
        happyscore += process_tweet(nlp, tweet, posWords, negWords)
    print("happiness tweets score : %f"%happyscore)


