import MySQLdb
import argparse
import json
import re
import time
from httplib import IncompleteRead

from tweepy import OAuthHandler
from tweepy.streaming import StreamListener, Stream

search_word = "trump"
db = MySQLdb.connect(host="microservicesass2.cbrsqtjo1q6h.us-west-2.rds.amazonaws.com", user="dan",
                     passwd="1234qwer", db="ass2")
cur = db.cursor()


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


class Twitter_Streamer(StreamListener):

    def on_data(self, data):
        dataset = json.loads(data)
        text = clean_tweet(dataset["text"]).replace("'", "")
        query = "INSERT INTO sentences (sentence, source, time, tweet_tag) VALUES ('" + text + "', 'twitter', '" + str(
            get_current_time()) + "', '" + search_word + "');"
        cur.execute(query)
        cur.execute("COMMIT")

    def on_error(self, status):
        print(status)
        return True


def my_main():
    clear_old_data_query = "DELETE FROM sentences"
    cur.execute(clear_old_data_query)
    cur.execute("COMMIT")
    args = get_parser().parse_args()
    auth = OAuthHandler("HqQlPfDvsu6oOVKcbSaC3dwy6", "Nr801nZ9gJoq5D6x1cQewFJeHDBnyI2IqUsYVePv7sQLLLjwxU")
    auth.set_access_token("2344102761-3D84t8gRyGEE2N9tBM99n8oTjGMdDJb12lIAWJ9",
                          "MEZtBsCwbFjrku0JOnggvlGmqB2O8x8gBC7s65wkjkJGx")
    while True:
        try:
            twitter_stream = Stream(auth, Twitter_Streamer(args.data_dir))
            twitter_stream.filter(track=[search_word])
        except IncompleteRead:
            continue


def get_current_time():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    my_main()
