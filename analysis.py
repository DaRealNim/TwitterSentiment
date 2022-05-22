import pickle
import stanza
import os
import pickle
import string
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

NEGATIONS = ["PAS", "GUÈRE", "JAMAIS", "NI"]

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

def process_word(word):
    for symbol in string.punctuation:
        word.replace(symbol, "")
    return word.upper()

def sentence_contains_ironic_adjective(words:list) -> bool:
    for index in range(1, len(words) - 1):
        preword, word, nextword = words[index-1], words[index], words[index+1]
        # print(f"{preword.text} {word.text} ({word.upos}) {nextword.text}")
        if preword.text == "\"" and nextword.text == "\"" and word.upos == "ADJ":
              return True
    return False

def process_sentence(stz_sentence, posWords, negWords):
    sentence_score = 0
    irony = sentence_contains_ironic_adjective(stz_sentence.words)
    negativemodscount = {}
    # first pass for negations
    for stz_word in stz_sentence.words:
        w = process_word(stz_word.text)
        if w in NEGATIONS:
            if stz_word.deprel is not None and "mod" in stz_word.deprel:
                if stz_word.head not in negativemodscount:
                    negativemodscount[stz_word.head] = 0
                negativemodscount[stz_word.head] += 1

    # second pass for word scores and to apply negations
    for stz_word in stz_sentence.words:
        w = process_word(stz_word.text)
        wordscore = 0
        for negword in negWords:
            if negword == w or (negword.endswith("*") and w.startswith(negword[:-1])):
                wordscore = -negWords[negword]
                break
        for posword in posWords:
            if posword == w or (posword.endswith("*") and w.startswith(posword[:-1])):
                wordscore = posWords[posword]
                break
        nNegativeMods = 0 if stz_word.id not in negativemodscount else negativemodscount[stz_word.id]
        wordscore *= pow(-1, nNegativeMods)
        sentence_score += wordscore
    if irony:
        sentence_score *= -1
    return sentence_score

def process_text(nlp, text, posWords, negWords):
    doc = nlp(text)
    text_score = 0
    for sentence in doc.sentences:
        text_score += process_sentence(sentence, posWords, negWords)
    # very basic irony detection
    if text.endswith("/s"):
        text_score *= -1
    return text_score



def openTestTweets():
    with open("exemple_datasets/bonheur.lst", "rb") as bonheurFile:
       bonheurTweets = pickle.load(bonheurFile)
    with open("exemple_datasets/haine.lst", "rb") as haineFile:
       haineTweets = pickle.load(haineFile)
    with open("exemple_datasets/ironique.lst", "rb") as ironieFile:
       ironieTweets = pickle.load(ironieFile)
    with open("exemple_datasets/negations.lst", "rb") as negationsFile:
       negationTweets = pickle.load(negationsFile)
    
    return (haineTweets, bonheurTweets, ironieTweets, negationTweets)

if __name__ == "__main__":
    nlp = stanza.Pipeline(lang='fr', processors="tokenize,mwt,pos,depparse,lemma", dir=os.getenv("DATA_DIR"))

    print("\n\n=======================\n")
    posWords, negWords = getNegAndPosWords()
    haineTweets, bonheurTweets, ironieTweets, negationTweets = openTestTweets()

    print("Test d'ironie:")
    for tweet in ironieTweets:
        print(tweet["text"] + " : " + str(process_tweet(nlp, tweet, posWords, negWords)))
    print("")
    print("Test de négations:")
    for tweet in negationTweets:
        print(tweet["text"] + " : " + str(process_tweet(nlp, tweet, posWords, negWords)))
    print("")
    hatescore = 0
    for tweet in haineTweets:
        hatescore += process_tweet(nlp, tweet, posWords, negWords)
    print("Score de 100 tweets comportant #hate : %f"%hatescore)

    happyscore = 0
    for tweet in bonheurTweets:
        happyscore += process_tweet(nlp, tweet, posWords, negWords)
    print("Score de 100 tweets comportant #bonheur : %f"%happyscore)

