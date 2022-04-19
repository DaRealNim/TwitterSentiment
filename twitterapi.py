import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = ""
with open(".bearertoken") as f:
    bearer_token = f.read().strip()

search_url = "https://api.twitter.com/2/tweets/search/recent?"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def searchTweets(hashtags, untilId):
    query_params = {
        'query' : '(%s -is:retweet)'%hashtags,
        'tweet.fields': 'author_id,lang',
        'max_results': 100,
    }
    if untilId != "":
        query_params["until_id"] = untilId
    return connect_to_endpoint(search_url, query_params)


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    for tweet in json_response["data"]:
        print(tweet["text"] + "\n")

if __name__ == "__main__":
    main()