import tweepy
import csv
import re
import json
from textblob import TextBlob

#Authentication
consumer_key="L0YdSokeGD14UGtfBKrexHMYl"
consumer_secret="NOsLL52yXpbDb5kNWx3CeltouydERnWGzmkTu6drxNXSLVYUsG"
access_token="826558986266804227-O7XFdDVLMkYIf6BFNgfSNEJowJiKNz5"
access_token_secret="0DMra9GSN9F5f1vidbcYruZjPSDdjxgH56chLYx3bKHoZ"

#Authentication
def dump_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=20)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(alltweets) < 200:
        print
        "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=20, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(
        "...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    # write the csv


def classify_is_pizza():
    return True

def find_date_location():
    return "1/27/2018", "35-2064"


if __name__ == '__main__':
    # pass in the username of the account you want to download
    dump_tweets("RITFreeFood")

