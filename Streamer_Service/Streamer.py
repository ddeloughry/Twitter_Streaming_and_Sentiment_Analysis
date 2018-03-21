import argparse
import json
import re
import string

import pika
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener, Stream

search_word = "maga"


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


class Streamer(StreamListener):
    def __init__(self, data_dir, query):
        super(Streamer, self).__init__()

    # query_fname = format_filename(query)
    # self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\/\/\S+)", " ", tweet).split())

    def on_data(self, data):
        dataset = json.loads(data)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'
                                                                       # , port=3000
                                                                       ))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=self.clean_tweet(dataset["text"]))
        # connection.close()

    #     try:
    #         with open(self.outfile, 'a') as f:
    #             f.write(data)
    #             print(data)
    #             return True
    #     except BaseException as e:
    #         print("Error on_data: %s" % str(e))
    #         time.sleep(5)
    #     return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


def my_main():
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler("HqQlPfDvsu6oOVKcbSaC3dwy6", "Nr801nZ9gJoq5D6x1cQewFJeHDBnyI2IqUsYVePv7sQLLLjwxU")
    auth.set_access_token("2344102761-3D84t8gRyGEE2N9tBM99n8oTjGMdDJb12lIAWJ9",
                          "MEZtBsCwbFjrku0JOnggvlGmqB2O8x8gBC7s65wkjkJGx")
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, Streamer(args.data_dir, args.query))
    twitter_stream.filter(track=[search_word])


if __name__ == '__main__':
    my_main()
