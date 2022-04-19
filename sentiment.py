import stanza
import os
import twitterapi

nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment', dir=os.getenv("TS_DATA"))

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
