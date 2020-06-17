import csv
import json

import tweepy
import threading, logging, time
from kafka import SimpleProducer, SimpleClient, SimpleConsumer, KafkaClient, KafkaProducer, KafkaConsumer
import string
import re


consumer_key = 'hL3hXKTgAElnMxSXoYyAmQQ5z'
consumer_secret = 'ecL8pxpufQqPmqMplDvbMqyrZOyprvur5xsy9pPXAJ4IZ7QqSe'
access_token = '1252138135477239808-dq1QTxj6dAd8c7yletPtaHpEqc1UHX'
access_token_secret = 'mGx3dZ4x35JX8YpDTwQpOXFzsnxidxt5MM6h51Foz9jQg'

mytopic='twitterstream'

class StdOutListener(tweepy.streaming.StreamListener):

    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.limit = 10
    def on_data(self, raw_data):
        """Called when raw data is received from connection. Overridden to avoid tweepy parsing data"""
        if (time.time() - self.start_time) < self.limit:
            all_data = json.loads(raw_data)
            username = all_data["user"]["screen_name"]
            check_location = all_data["user"]["location"]
            fetch_location = "Not available" if check_location is None else check_location
            check_hashtag_exists = all_data["entities"]["hashtags"]
            try:
                if check_hashtag_exists != [] and fetch_location != "Not available":
                    hashtags = all_data["entities"]["hashtags"][0]["text"]
                    tweet_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int((all_data['timestamp_ms'])) / 1000))
                    tweet = ' '.join(
                        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", all_data["text"]).split())
                    print(hashtags)
                    print(username)
                    print(tweet)
                    print(fetch_location)
                    print(tweet_time)
                    print("--------------------------")
                    msg = str(hashtags) + ',' + str(username) + ',' + str(tweet) + ',' + str(fetch_location) + ',' + str(tweet_time)
                    producer = KafkaProducer(bootstrap_servers='localhost:9092')
                    producer.send(topic=mytopic, value=msg.encode('utf-8'))
                    producer.flush()

                    print("DONE.")


                    return True
                return True
            except Exception as e:
                print(e)
                return True
        return False


if __name__ == "__main__":
    # Create an instance of the AuthHandler object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Create an instance of the Listener object
    listener = StdOutListener()
    # Create an instance of a twitter Stream (what actually pulls data in). Pass it your auth
    # and listener objects (listener will be given the incoming stream the data)
    stream = tweepy.Stream(auth, listener)
    # Call the stream filter. Can filter on users ('follow' param), keywords ('track'), and locations
    # Can use any combinations of those three params. Considered 'OR'ed together
    stream.filter(track=["corona"], languages=['en'], encoding='utf-8')
