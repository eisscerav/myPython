from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import json


class Review:
    def __init__(self, text, score):
        self.text = text
        self.score = score
        self.sentiment = self.get_sentiment()

    def get_sentiment(self):
        if self.score > 3:
            return 'POSITIVE'
        elif self.score < 3:
            return 'NEGATIVE'
        else:
            return 'NEUTRAL'


def demo_test_split():
    reviews = []
    with open(r'data/Books_small.json') as f:
        for each in f:
            data = json.loads(each)
            text = data.get('reviewText')
            score = data.get(r'overall')
            reviews.append(Review(text, score))

    # prepare data
    train, test = train_test_split(reviews, test_size=0.2, random_state=42)
    train_x = [x.text for x in train]
    train_y = [x.sentiment for x in train]
    test_x = [x.text for x in test]
    test_y = [x.sentiment for x in test]
    vectorizer = CountVectorizer()
    fit_vec = vectorizer.fit_transform(train_x)
    print(data)


if __name__ == '__main__':
    demo_test_split()
