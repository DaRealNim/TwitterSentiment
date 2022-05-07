import stanza
import os
import twitterapi
import pickle
import dictanal
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

print(os.getenv("DATA_DIR"))

nlp = stanza.Pipeline(lang='fr', processors="tokenize", dir=os.getenv("DATA_DIR"))

posWords, negWords = dictanal.getNegAndPosWords()

print("\n==========================\n")

while True:
    
    hashtags = input("Hashtags: ")
    tweetBatches = int(input("Number of batches (100/batch): "))

    untilId = ""
    tweets = []
    for i in range(tweetBatches):
        # print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
        tweets += twitterapi.searchTweets(hashtags, untilId)["data"]
        # print("Got %d tweets"%len(tweets))
        # print("Last tweet :",tweets[-1])
        if (len(tweets) < (i+1)*100):
            # print("No more tweets")
            break
        untilId = tweets[-1]["id"]

    # print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")

    tweets = list(filter(lambda e: e["lang"] == "fr", tweets))
    print("Kept %d french tweets"%len(tweets))
    total = 0
    for tweet in tweets:
        total += dictanal.process_tweet(nlp, tweet, posWords, negWords)
    # total /= len(tweets)
    print("Result :", total)
