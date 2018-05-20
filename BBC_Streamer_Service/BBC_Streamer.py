import time

import MySQLdb
import feedparser


def my_main():
    bbc = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml?edition=uk')
    db = MySQLdb.connect(host="microass2.cbrsqtjo1q6h.us-west-2.rds.amazonaws.com", user="dan",
                         passwd="1234qwer", db="ass2")
    cur = db.cursor()
    while True:
        try:
            for each in bbc['entries']:
                text = each['summary'].replace("'", "")
                cur.execute("INSERT INTO sentences (sentence, source, time) VALUES (%s, 'bbc', %s);",
                            (text, int(get_current_time())))
                cur.execute("COMMIT")
        except UnicodeEncodeError:
            continue


def get_current_time():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    my_main()
