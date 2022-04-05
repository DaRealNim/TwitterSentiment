import stanza
import twitterapi

nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment', dir="/home/Nim/sdcard/stanza_resources")

while True:
    hashtags = input("Hashtags: ")
    tweets = twitterapi.searchTweets(hashtags)
    total = 0
    for tweet in tweets["data"]:
        doc = nlp(tweet["text"])
        phrasetotal = 0
        for s in doc.sentences:
            phrasetotal += s.sentiment
        phrasetotal /= len(doc.sentences)
        total += phrasetotal
    total /= len(tweets["data"])
    print(total)