import stanza
import os
import twitterapi
import pickle
import analysis
import warnings
import argparse

warnings.filterwarnings("ignore", category=UserWarning)

print(os.getenv("DATA_DIR"))

nlp = stanza.Pipeline(lang='fr', processors="tokenize,mwt,pos,depparse,lemma", dir=os.getenv("DATA_DIR"))

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
                    tweets += twitterapi.searchTweets(hashtags, untilId)["data"]
                    if (len(tweets) < (i+1)*100):
                        break
                    untilId = tweets[-1]["id"]
                print("%d tweets récents français récupérés"%len(tweets))
                total = 0
                for tweet in tweets:
                    total += analysis.process_text(nlp, tweet["text"], words)
                # total /= len(tweets)
                print("Resultat :", total)
                print()
            else:
                text = input("Texte: ")
                print("Résultat :", analysis.process_text(nlp, text, words, verbose=True))
                print()
    except KeyboardInterrupt:
        print("\n\nInterruption détectée.")
        print("Au revoir!")
        exit(0)