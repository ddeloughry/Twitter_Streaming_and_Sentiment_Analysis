from ast import literal_eval

import pika
from pymongo import MongoClient
from textblob import TextBlob


class Analysis:

    def get_tweet_sentiment(self, tweet):
        con = MongoClient('localhost')
        db = con.tweets_db
        coll = db.tweets_coll
        tweet_dict = literal_eval(tweet)
        analysis = TextBlob(tweet)
        score = round(analysis.sentiment.subjectivity, 2)
        tweet_dict["score"] = score
        coll.insert_one(tweet_dict)

    def get_tweets(self):
        tweets = []
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='tweets')

        def callback(ch, method, properties, tweet):
            tweet = tweet.decode()
            self.get_tweet_sentiment(tweet)

        channel.basic_consume(callback, queue='tweets', no_ack=True)

        print("Waiting for tweets...")
        channel.start_consuming()
        return tweets


def my_main():
    api = Analysis()
    tweets = api.get_tweets()


if __name__ == '__main__':
    my_main()
