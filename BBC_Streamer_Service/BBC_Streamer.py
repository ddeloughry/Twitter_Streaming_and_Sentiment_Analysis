import feedparser
import pika


def my_main():
    bbc = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml?edition=uk')
    count = 0

    for each in bbc['entries']:
        news_dict = dict()
        news_dict["bbc"] = each['summary']
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='bbc')
        channel.basic_publish(exchange='',
                              routing_key='bbc',
                              body=str(news_dict))
        count += 1
        print(news_dict)


if __name__ == '__main__':
    my_main()
