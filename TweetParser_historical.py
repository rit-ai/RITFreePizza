import tweepy
import pandas as pd

import re

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
    while len(new_tweets) > 0:
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
    output = pd.DataFrame(columns=["Tweet_id","data_source","Location", "Event_Name", "Pizza_Status", "Event_Date", "Sent_Date", "Text"])
    for each_tweet in outtweets:
        is_pizza = classify_is_pizza(each_tweet[2].decode())
        event_date, loc = find_date_location(each_tweet)
        output = output.append(pd.DataFrame([[each_tweet[0], "tweet", loc, None, is_pizza, event_date, each_tweet[1], each_tweet[2].decode()]], columns=["Tweet_id", "data_source","Location", "Event_Name", "Pizza_Status", "Event_Date", "Sent_Date","Text"]))

    writer = pd.ExcelWriter('output.xlsx')
    output.to_excel(writer, "Twitter_data")
    writer.save()

def classify_is_pizza(tweet):
    return "pizza" in tweet

def find_event_name():
    pass

def find_date_location(tweet):
    return "1/27/2018", "35-2064"


if __name__ == '__main__':
    # pass in the username of the account you want to download
    dump_tweets("RITFreeFood")

