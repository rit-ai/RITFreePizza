from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import re
import json
from textblob import TextBlob

#Authentication
consumer_key="L0YdSokeGD14UGtfBKrexHMYl"
consumer_secret="NOsLL52yXpbDb5kNWx3CeltouydERnWGzmkTu6drxNXSLVYUsG"
access_token="826558986266804227-O7XFdDVLMkYIf6BFNgfSNEJowJiKNz5"
access_token_secret="0DMra9GSN9F5f1vidbcYruZjPSDdjxgH56chLYx3bKHoZ"

f = open('TwitterText.txt', 'w')
#listener class that streams data
class listener(StreamListener):

    def on_data(self, data):
        #Opening a file to be used within the class
        json_load = json.loads(data)
        texts = json_load['text']
        timestamp = json_load['timestamp_ms']
        coded = texts.encode('utf-8')
        s = str(coded)
        print(s)
##        blob = TextBlob(s)
##        blob.tags
##        blob.noun_phrases
##
##        for sentence in blob.sentences:
##            print(sentence.sentiment.polarity)
##        ##print(timestamp)
##        f.write(s+'\n')
        #tweet = data.split(',"text":"')[1].split('","source')[0]
            
      #  print("writing. . .")
       # f.write(tweet)
        return(True)
        f.close()
        

    def on_error(self, status):
        print (status)



#Authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Stream listener class is instatiated here, authentication passed
twitterStream = Stream(auth, listener())
#RITFreeFood
twitterStream.filter(follow=["jonennin_lock"])
##twitterStream.sample(languages=['en'])
twitterStream.filter(languages=["en"])
