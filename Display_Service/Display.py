import MySQLdb
import time

from flask import Flask

app = Flask(__name__)


@app.route("/sentiment")
def print_to_browser():
    db = MySQLdb.connect(host="microservicesass2.cbrsqtjo1q6h.us-west-2.rds.amazonaws.com", user="dan",
                         passwd="1234qwer", db="ass2")
    cur = db.cursor()
    minute_ago = get_current_time() - 60000
    tweet_query = "SELECT tweet_tag FROM sentences WHERE source='twitter' GROUP BY tweet_tag"
    cur.execute(tweet_query)
    tweet_tag = cur.fetchone()[0]
    twitter_average_query = "SELECT AVG(sentiment) FROM sentences WHERE source='twitter' && time>=" + str(minute_ago)
    cur.execute(twitter_average_query)
    twitter_average = cur.fetchone()[0]
    if twitter_average is None:
        twitter_average = 0
    bbc_average_query = "SELECT AVG(sentiment) FROM sentences WHERE source='bbc' "
    cur.execute(bbc_average_query)
    bbc_average = cur.fetchone()[0]
    if bbc_average is None:
        bbc_average = 0
    string = "<h1>Data-Driven Microservices</h1><h2>Assignment 1 - Twitter Sentiment Analysis</h2>"
    string += '<p>The average sentiment score for <strong>"' + tweet_tag
    string += '"</strong> on Twitter based on Tweets, in the past minute is '
    string += '<strong>' + str(twitter_average) + '</strong></p>'
    string += 'The average sentiment score for the <strong>"BBC RSS"</strong> feed is '
    string += '<strong>' + str(bbc_average) + '</strong> '
    return string


def is_under_minute(param):
    diff = get_current_time() - param
    if diff < 60000:
        return True
    else:
        return False


def get_current_time():
    return int(round(time.time() * 1000))


def my_main():
    print("Please wait while tweets are analysed:...")
    print("Please wait while BCC RSS posts are analysed:...")
    app.run(host='0.0.0.0', port=3000)


if __name__ == '__main__':
    my_main()
