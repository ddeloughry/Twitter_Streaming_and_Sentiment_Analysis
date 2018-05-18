import MySQLdb

from textblob import TextBlob


class Analysis:
    def get_sentence_sentiment(self, sentence):
        analysis = TextBlob(sentence)
        score = round(analysis.sentiment.subjectivity, 2)
        return score

    def get_sentences(self):
        while True:
            db = MySQLdb.connect(host="microass2.cbrsqtjo1q6h.us-west-2.rds.amazonaws.com", user="dan",
                                 passwd="1234qwer", db="ass2")
            cur = db.cursor()
            cur.execute("SELECT id, sentence FROM sentences WHERE sentiment IS NULL;")
            for each in cur:
                score = int(self.get_sentence_sentiment(each[1]))
                cur.execute("UPDATE sentences SET sentiment=%s WHERE id=%s AND sentiment IS NULL;", (score, each[0]))
                cur.execute("COMMIT")


def my_main():
    Analysis().get_sentences()


if __name__ == '__main__':
    my_main()
