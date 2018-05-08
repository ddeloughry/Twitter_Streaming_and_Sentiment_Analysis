from ast import literal_eval
from threading import Thread

import pika
from pymongo import MongoClient
from textblob import TextBlob


def get_sentence_sentiment(sentence, sentence_type):
    con = MongoClient('localhost')
    db = con.micro_db
    if sentence_type == "tweets":
        coll = db.tweets
    else:
        coll = db.bbc
    dictionary = literal_eval(sentence)
    analysis = TextBlob(sentence)
    score = round(analysis.sentiment.subjectivity, 2)
    dictionary["score"] = score
    coll.insert_one(dictionary)


class Analysis:

    def get_sentences(self, sentence_type):
        tweets = []
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=sentence_type)

        def callback(ch, method, properties, sentence):
            sentence = sentence.decode()
            print(sentence)
            get_sentence_sentiment(sentence, sentence_type)
            pass

        channel.basic_consume(callback, queue=sentence_type, no_ack=True)
        print("Waiting for sentences...")
        channel.start_consuming()
        return tweets


def func1():
    Analysis().get_sentences("bbc")


def func2():
    Analysis().get_sentences("tweets")


def my_main():
    Thread(target=func1).start()
    Thread(target=func2).start()


if __name__ == '__main__':
    my_main()
