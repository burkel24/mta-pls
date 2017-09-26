import os
import json
import time

from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream

class TweetListener(StreamListener):
    tweet_buffer = []
    buffer_size = 500 # save to file every n tweets

    def __init__(self):
        try:
            os.makedirs('data')
        except:
            pass

    def on_data(self, data):
        self.tweet_buffer.append(data)
        if len(self.tweet_buffer) >= self.buffer_size:
            self.save_data()

    def on_error(self, status):
        print(status)

    def save_data(self):
        if len(self.tweet_buffer) == 0: return

        # TODO multithread this
        timestamp = int(time.time())
        tweets = self.tweet_buffer
        self.tweet_buffer = []
        filename = 'data/' + str(int(time.time())) + '-tweets.txt'

        with open(filename, 'w') as f:
            for tweet in tweets:
                f.write(json.dumps(tweet))


class TweetBot:
    # terms = ['#MTA', '@NYCT']
    terms = ['javascript']

    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret):
        self.listener = TweetListener()
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.stream = Stream(self.auth, self.listener)
        self.listen()

    def listen(self):
      self.stream.filter(track=self.terms)

if __name__ == '__main__':
    bot = TweetBot(os.environ['TWITTER_ACCESS'],
                   os.environ['TWITTER_ACCESS_SECRET'],
                   os.environ['TWITTER_CONSUMER'],
                   os.environ['TWITTER_CONSUMER_SECRET'])
