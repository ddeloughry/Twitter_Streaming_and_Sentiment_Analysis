import datetime

from dateutil import parser
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
search_name = ""
tw_times = []
score = 0


@app.route("/sentiment")
def print_to_browser():
    string = "<h1>Data-Driven Microservices</h1><h2>Assignment 1 - Twitter Sentiment Analysis</h2>"
    if search_name != "":
        string += '<p>The average sentiment score for "<strong>' + search_name + '</strong>" based on Tweets, in the ' \
                                                                                 'past minute is <strong>' + str(score) + '</strong></p>'
    else:
        string += "<p>Please run Streamer and Analysis services and restart Display service</p>"
    return string


def find_average(score):
    return score


def is_under_minute(param):
    date = parser.parse(param)
    now = datetime.datetime.now()
    diff = str(now - date)
    diff = diff.replace(":", ".")
    diff = diff.split(".")
    if int(diff[1]) >= 1 and int(diff[0]) == 0:
        return True
    else:
        return False


def my_main():
    print("Please wait while tweets are analysed:...")
    con = MongoClient('localhost')
    db = con.tweets_db
    tweets = db.tweets_coll
    tw = tweets.find()

    for each in tw:
        global search_name
        search_name = each["search_word"]
        if is_under_minute(each["time"]):
            tw_times.append(each["score"])
    total = 0

    for each in tw_times:
        total += each
    global score
    score = total / len(tw_times)
    score = round(score, 2)
    app.run(host='localhost', port=3000)


if __name__ == '__main__':
    my_main()
