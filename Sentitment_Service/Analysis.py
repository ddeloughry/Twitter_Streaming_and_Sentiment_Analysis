import pika


def my_main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, tweet):
        print(tweet)

    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=True)

    print("Waiting for tweets")
    channel.start_consuming()


if __name__ == '__main__':
    my_main()
