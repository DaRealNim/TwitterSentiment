import pickle
import stanza
import os
import pickle
import string
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

NEGATIONS = ["PAS", "GUÈRE", "JAMAIS", "NI"]

def getNegAndPosWords():
    suffixes = []
    with open("dicts/suffixes.txt") as suffixFile:
        suffixes = suffixFile.read().splitlines()
    with open("dicts/annotated.dict") as dictFile:
        lines = iter(dictFile.readlines())
        words = {}
        next(lines)
        c = 2
        try:
            while ((neg := next(lines).strip()) != "POSITIVE"):
                neg = neg.split("(")
                neg[0] = neg[0].strip()
                neg[1] = neg[1].replace(")", "")
                neg[1] = float(neg[1])
                if neg[0].endswith("*"):
                    # regexes[re.compile("^"+neg[0][:-1]+".*$")] = -neg[1]
                    words[neg[0][:-1]] = -neg[1]
                    for s in suffixes:
                        words[neg[0][:-1] + s.upper()] = -neg[1]
                else:
                    words[neg[0]] = -neg[1]
                c += 1
        
            while True:
                try:
                    pos = next(lines).strip()
                    c += 1
                    pos = pos.split("(")
                    pos[0] = pos[0].strip() 
                    pos[1] = pos[1].replace(")","")
                    pos[1] = float(pos[1])    
                    if pos[0].endswith("*"):
                        # regexes[re.compile("^"+pos[0][:-1]+".*$")] = pos[1]
                        words[pos[0][:-1]] = pos[1]
                        for s in suffixes:
                            words[pos[0][:-1] + s.upper()] = pos[1]
                    else:       
                        words[pos[0]] = pos[1]
                except StopIteration:
                    break
        except Exception as e:
            print(e)
            print("line %d"%c)
    dictFile.close()
    return (words)

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

def process_sentence(stz_sentence, words, verbose):
    sentence_score = 0
    irony = sentence_contains_ironic_adjective(stz_sentence.words)
    relevantwords = 0
    negativemodscount = {}
    sentimentwords = []
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
        verboseout = ""
        w = process_word(stz_word.text)
        if w == "FRANCE":
            continue

        if verbose: verboseout += "-> "+w+"\n"
        wordscore = words.get(w)
        if wordscore is None:
            # for reg in regexes:
            #     if reg.search(w) is not None:
            #         if verbose : verboseout += "Expression régulière " + w + " : " + reg.pattern + "\n"
            #         relevantwords += 1
            #         wordscore = regexes[reg]
            #         break
            pass
        else:
            sentimentwords.append((w, wordscore))
            relevantwords += 1


        wordscore = 0 if wordscore is None else wordscore
        
        nNegativeMods = 0 if stz_word.id not in negativemodscount else negativemodscount[stz_word.id]
        if verbose and nNegativeMods != 0: verboseout += "Affecté par " + str(nNegativeMods) + " négation(s)"
        wordscore *= pow(-1, nNegativeMods)
        if verbose and wordscore != 0: print(verboseout, "\n", w, ":", wordscore, "\n")
        sentence_score += wordscore
    # if relevantwords != 0:
    #     sentence_score /= relevantwords
    if irony:
        sentence_score *= -1

    return sentence_score, sentimentwords

def process_text(nlp, text, words, verbose=False):
    doc = nlp(text)
    text_score = 0
    sentimentwords = []
    for sentence in doc.sentences:
        score, usedwords = process_sentence(sentence, words, verbose)
        text_score += score
        sentimentwords += usedwords
    # text_score /= len(doc.sentences)
    # very basic irony detection
    if text.endswith("/s"):
        if verbose: print("-> /s indique l'ironie, inversion du score de la phrase")
        text_score *= -1
    return text_score, sentimentwords



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
    nlp = None
    try:
        if os.getenv("DATA_DIR") is None:
            nlp = stanza.Pipeline(lang='fr', processors="tokenize,mwt,pos,depparse,lemma")
        else:
            nlp = stanza.Pipeline(lang='fr', processors="tokenize,mwt,pos,depparse,lemma", dir=os.getenv("DATA_DIR"))
    except stanzacore.LanguageNotDownloadedError:
        print("[-] Erreur : impossible de charger les modèles stanzas.")
        print("Si vos modèles sont dans un dossier différent du chemin par defaut, paramétrez la variable \
        d'environnement DATA_DIR avec le chemin du dossier stanza_resources.")
        exit(1)

    print("\n\n=======================\n")
    words = getNegAndPosWords()
    haineTweets, bonheurTweets, ironieTweets, negationTweets = openTestTweets()

    print("Test d'ironie:")
    for tweet in ironieTweets:
        print(tweet["text"] + " : " + str(process_text(nlp, tweet["text"], words)))
    print("")
    print("Test de négations:")
    for tweet in negationTweets:
        print(tweet["text"] + " : " + str(process_text(nlp, tweet["text"], words)))
    print("")
    hatescore = 0
    for tweet in haineTweets:
        hatescore += process_text(nlp, tweet["text"], words)
    print("Score de 100 tweets comportant #hate : %f"%hatescore)

    happyscore = 0
    for tweet in bonheurTweets:
        happyscore += process_text(nlp, tweet["text"], words)
    print("Score de 100 tweets comportant #bonheur : %f"%happyscore)


