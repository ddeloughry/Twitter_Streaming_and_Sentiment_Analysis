import datetime

from dateutil import parser
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
twitter_search_name = ""
tweets_total_score = []
bbc_total_score = []
twitter_average = 0
bbc_average = 0


@app.route("/sentiment")
def print_to_browser():
    all_tweets = db.tweets.find()
    for each_tweets in all_tweets:
        global twitter_search_name
        twitter_search_name = each_tweets["search_word"]
        if is_under_minute(each_tweets["time"]):
            tweets_total_score.append(each_tweets["score"])
    number_of_tweets = 0
    if len(tweets_total_score) > 0:
        for each_tweets in tweets_total_score:
            number_of_tweets += each_tweets
        global twitter_average
        twitter_average = number_of_tweets / len(tweets_total_score)
    twitter_average = round(twitter_average, 2)

    all_bbc = db.bbc.find()
    for each_bbc in all_bbc:
        bbc_total_score.append(each_bbc["score"])
    number_of_news = 0
    if len(bbc_total_score) > 0:
        for each_bbc in bbc_total_score:
            number_of_news += each_bbc
        global bbc_average
        bbc_average = number_of_news / len(bbc_total_score)
    bbc_average = round(bbc_average, 2)

    string = "<h1>Data-Driven Microservices</h1><h2>Assignment 1 - Twitter Sentiment Analysis</h2>"
    if twitter_search_name != "":
        string += '<p>The average sentiment score for <strong>"' + twitter_search_name
        string += '"</strong>on Twitter based on Tweets, in the past minute is '
        string += '<strong>' + str(twitter_average) + '</strong></p>'
    else:
        string += '<p>Please run Streamer and Analysis services and restart Display service</p>'
    string += 'The average sentiment score for the <strong>"BBC RSS"</strong> feed is '
    string += '<strong>' + str(bbc_average) + '</strong> '
    return string


def is_under_minute(param):
    date = parser.parse(param)
    now = datetime.datetime.now()
    diff = str(now - date)
    diff = diff.replace(":", ".")
    diff = diff.split(".")
    if int(diff[1]) >= 1 and int(diff[0].split(" ")[0]) == 0:
        return True
    else:
        return False


def my_main():
    con = MongoClient('localhost')
    global db
    db = con.micro_db
    print("Please wait while tweets are analysed:...")
    print("Please wait while BCC RSS posts are analysed:...")
    app.run(host='localhost', port=3000)


if __name__ == '__main__':
    my_main()
