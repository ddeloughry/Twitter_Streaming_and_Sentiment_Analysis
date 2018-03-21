from flask import Flask

app = Flask(__name__)


@app.route("/sentiment")
def print_to_browser():
    return "<h1>Data-Driven Microservices</h1>" \
           "<h2>Assignment 1 - Twitter Sentiment Analysis</h2>" \
           '<p>The average sentiment score for "<strong>maga</strong>" based on Tweets is <strong>0.72</strong></p>'


def my_main():
    app.run(host='localhost', port=3000)


if __name__ == '__main__':
    my_main()
