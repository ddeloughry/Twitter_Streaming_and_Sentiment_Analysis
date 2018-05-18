import MySQLdb
import time

from flask import Flask

app = Flask(__name__)


@app.route("/sentiment")
def print_to_browser():
    db = MySQLdb.connect(host="microass2.cbrsqtjo1q6h.us-west-2.rds.amazonaws.com", user="dan",
                         passwd="1234qwer", db="ass2")
    cur = db.cursor()
    cur.execute("SELECT tweet_tag FROM sentences WHERE source='twitter' GROUP BY tweet_tag;")
    tweet_tag = cur.fetchone()[0]
    cur.execute("SELECT AVG(sentiment) FROM sentences WHERE source='twitter';")
    twitter_average = cur.fetchone()[0]
    if twitter_average is None:
        twitter_average = 0
    cur.execute("SELECT AVG(sentiment) FROM sentences WHERE source='bbc';")
    bbc_average = cur.fetchone()[0]
    if bbc_average is None:
        bbc_average = 0
    string = "<h1>Data-Driven Microservices</h1><h2>Assignment 1 - Twitter Sentiment Analysis</h2>"
    string += '<p>The average sentiment score for <strong>"' + tweet_tag
    string += '"</strong> on Twitter based on Tweets, is '
    string += '<strong>' + str(twitter_average) + '</strong></p>'
    string += 'The average sentiment score for the <strong>"BBC RSS"</strong> feed is '
    string += '<strong>' + str(bbc_average) + '</strong> '
    return string


def my_main():
    print("Please wait while tweets are analysed:...")
    print("Please wait while BCC RSS posts are analysed:...")
    app.run(host='0.0.0.0', port=3000)


if __name__ == '__main__':
    my_main()
