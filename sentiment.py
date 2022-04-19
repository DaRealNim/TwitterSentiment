import stanza
import os
import twitterapi
import pickle

print(os.getenv("DATA_DIR"))

nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment', dir=os.getenv("DATA_DIR"))

while True:
    
    hashtags = input("Hashtags: ")
    tweetBatches = int(input("Number of batches (100/batch): "))

    untilId = ""
    tweets = []
    for i in range(tweetBatches):
        print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
        tweets += twitterapi.searchTweets(hashtags, untilId)["data"]
        print("Got %d tweets"%len(tweets))
        print("Last tweet :",tweets[-1])
        untilId = tweets[-1]["id"]

    print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")

    for tweet in tweets:
        if tweet["lang"] != "fr":
            tweets.remove(tweet)
    total = 0
    for tweet in tweets:
        doc = nlp(tweet["text"])
        phrasetotal = 0
        for s in doc.sentences:
            phrasetotal += s.sentiment
        phrasetotal /= len(doc.sentences)
        total += phrasetotal
    total /= len(tweets)
    print("Result :", total)
