import argparse
import datetime
import json
import re

import pika
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener, Stream

search_word = "brexit"


def get_parser():
    pparser = argparse.ArgumentParser(description="Twitter Downloader")
    pparser.add_argument("-q",
                         "--query",
                         dest="query",
                         help="Query/Filter",
                         default='-')
    pparser.add_argument("-d",
                         "--data-dir",
                         dest="data_dir",
                         help="Output/Data Directory")
    return pparser


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\/\/\S+)", " ", tweet).split())


class Streamer(StreamListener):

    def on_data(self, data):
        dataset = json.loads(data)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='tweets')
        tweet_dict = dict()
        tweet_dict["search_word"] = search_word
        tweet_dict["tweet_text"] = clean_tweet(dataset["text"])
        tweet_dict["time"] = str(datetime.datetime.now())
        channel.basic_publish(exchange='',
                              routing_key='tweets',
                              body=str(tweet_dict))

    def on_error(self, status):
        print(status)
        return True


def my_main():
    args = get_parser().parse_args()
    auth = OAuthHandler("HqQlPfDvsu6oOVKcbSaC3dwy6", "Nr801nZ9gJoq5D6x1cQewFJeHDBnyI2IqUsYVePv7sQLLLjwxU")
    auth.set_access_token("2344102761-3D84t8gRyGEE2N9tBM99n8oTjGMdDJb12lIAWJ9",
                          "MEZtBsCwbFjrku0JOnggvlGmqB2O8x8gBC7s65wkjkJGx")
    print("Streaming...")
    twitter_stream = Stream(auth, Streamer(args.data_dir))
    twitter_stream.filter(track=[search_word])


if __name__ == '__main__':
    my_main()
