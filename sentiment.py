import stanza
import os
import twitterapi
import pickle
import analysis
import warnings
import argparse
import math
import stanza.pipeline.core as stanzacore

warnings.filterwarnings("ignore", category=UserWarning)

print(os.getenv("DATA_DIR"))

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

words = analysis.getNegAndPosWords()

print("\n==========================\n")
twittermode = True
while True:
    print("[1] Analyser un sujet sur twitter")
    print("[2] Tester l'analyse de sentiment sur une phrase")
    print("[3] Quitter")
    choice = input("choix> ")
    if choice == "1":
        twittermode = True
    if choice == "2":
        twittermode = False
    if choice == "3":
        exit(0)
    
    print("(utilisez CTRL+C pour quitter)")

    try:
        while True:
            
            if twittermode:
                hashtags = input("Hashtags et/ou termes de recherche: ")
                tweetBatches = int(input("Nombre de lots max (100 tweets/lots): "))

                untilId = ""
                tweets = []
                for i in range(tweetBatches):
                    res = twitterapi.searchTweets(hashtags, untilId)
                    if "data" not in res:
                        print("[!] Pas de tweets correspondants")
                        continue
                    tweets += res["data"]
                    if (len(tweets) < (i+1)*100):
                        break
                    untilId = tweets[-1]["id"]
                if len(tweets) == 0:
                    continue
                print("%d tweets récents français récupérés"%len(tweets))
                sentimentwords = []
                total = 0
                mostnegtweet = ""
                mostpostweet = ""
                mostnegtweetscore = math.inf
                mostpostweetscore = -math.inf
                for tweet in tweets:
                    score, usedwords = analysis.process_text(nlp, tweet["text"], words)
                    if score > mostpostweetscore:
                        mostpostweetscore = score
                        mostpostweet = tweet["text"]
                    if score < mostnegtweetscore:
                        mostnegtweetscore = score
                        mostnegtweet = tweet["text"]
                    total += score
                    sentimentwords += usedwords
                # total /= len(tweets)
                print("========= Resultat :", total, "=========")
                sentimentwords.sort(key=lambda x: x[1])
                poswords = list(map(lambda x: x[0], filter(lambda x: x[1]>0, sentimentwords)))
                negwords = list(map(lambda x: x[0], filter(lambda x: x[1]<0, sentimentwords)))
                mostcommonposword = max(poswords, key=poswords.count)
                mostcommonnegword = max(negwords, key=negwords.count)
                print("\nTweet le plus négatif (score %d):"%mostnegtweetscore)
                print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
                print(mostnegtweet)
                print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
                print("\nTweet le plus positif (score %d):"%mostpostweetscore)
                print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
                print(mostpostweet)
                print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
                print("\nMot le plus négatif reconnu :", sentimentwords[0])
                print("Mot le plus positif reconnu :", sentimentwords[-1])
                print("Mot négatif le plus courant :", mostcommonnegword)
                print("Mot positif le plus courant :", mostcommonposword)

                print("=============================================")
                print("\n"*3)
            else:
                text = input("Texte: ")
                score, usedwords = analysis.process_text(nlp, text, words, verbose=True)
                print("Résultat :", score)
                print()
    except KeyboardInterrupt:
        print("\n\nInterruption détectée.")
        print("Au revoir!")
        exit(0)
