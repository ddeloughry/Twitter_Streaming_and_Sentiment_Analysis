import MySQLdb
import datetime
import feedparser
import time


def my_main():
    bbc = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml?edition=uk')
    db = MySQLdb.connect(host="microservicesass2.cbrsqtjo1q6h.us-west-2.rds.amazonaws.com", user="dan",
                         passwd="1234qwer", db="ass2")
    cur = db.cursor()

    for each in bbc['entries']:
        text = each['summary'].replace("'", "")
        query = "INSERT INTO sentences (sentence, source, time) VALUES ('" + text + "', 'bbc', '" + str(
            get_current_time()) + "');"
        cur.execute(query)
        cur.execute("COMMIT")

        # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # channel = connection.channel()
        # channel.queue_declare(queue='bbc')
        # channel.basic_publish(exchange='',
        #                       routing_key='bbc',
        #                       body=str(news_dict))
        # count += 1
        # print(news_dict)


def get_current_time():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    my_main()
