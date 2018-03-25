import datetime

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
search_name = ""
tw_dict = dict()


@app.route("/sentiment")
def print_to_browser():
    string = "<h1>Data-Driven Microservices</h1><h2>Assignment 1 - Twitter Sentiment Analysis</h2>"
    if search_name != "":
        string += '<p>The average sentiment score for "<strong>' + search_name + '</strong>" based on Tweets is ' \
                                                                                 '<strong>0.72</strong></p> '
    else:
        string += "<p>Please run Streamer and Analysis services and restart Display service</p>"
    return string


def my_main():
    con = MongoClient('localhost')
    db = con.tweets_db
    tweets = db.tweets_coll
    tw = tweets.find()
    now = datetime.datetime.now()
    for each in tw:
        global search_name
        search_name = each["search_word"]
        print(each["tweet_text"])
    app.run(host='localhost', port=3000)


if __name__ == '__main__':
    my_main()
