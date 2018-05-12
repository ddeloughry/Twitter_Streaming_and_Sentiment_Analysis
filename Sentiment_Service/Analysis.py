import MySQLdb

from textblob import TextBlob


class Analysis:
    def get_sentence_sentiment(self, sentence):
        analysis = TextBlob(sentence)
        score = round(analysis.sentiment.subjectivity, 2)
        return score

    def get_sentences(self):
        while True:
            db = MySQLdb.connect(host="microservicesass2.cbrsqtjo1q6h.us-west-2.rds.amazonaws.com", user="dan",
                                 passwd="1234qwer", db="ass2")
            cur = db.cursor()
            query = "SELECT id, sentence FROM sentences WHERE sentiment IS NULL "
            cur.execute(query)
            for each in cur:
                score = self.get_sentence_sentiment(each[1])
                update_query = "UPDATE sentences SET sentiment='" + str(score) + "' WHERE id='" + str(
                    each[0]) + "' AND sentiment IS NULL;"
                cur.execute(update_query)
                cur.execute("COMMIT")


def my_main():
    Analysis().get_sentences()


if __name__ == '__main__':
    my_main()
