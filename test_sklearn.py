from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import datasets
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


def demo_cls_nlp():
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
    # train_x_vector = vectorizer.fit_transform(train_x)  # sparse matrix
    vectorizer.fit(train_x)
    train_x_vector = vectorizer.transform(train_x)
    test_x_vector = vectorizer.transform(test_x)
    train_array = train_x_vector.toarray()

    # classification SVM
    from sklearn import svm
    clf_svm = svm.SVC(kernel='linear')
    clf_svm.fit(train_x_vector, train_y)
    y0 = clf_svm.predict(test_x_vector[0])

    # Decision tree
    from sklearn.tree import DecisionTreeClassifier
    clf_dec = DecisionTreeClassifier()
    clf_dec.fit(train_x_vector, train_y)
    y3 = clf_dec.predict(test_x_vector[3])

    # Naive Bayes
    from sklearn.naive_bayes import GaussianNB
    clf_gnb = GaussianNB()
    clf_gnb.fit(train_x_vector.toarray(), train_y)
    y5 = clf_gnb.predict(test_x_vector[5].toarray())

    # Logistical regression
    from sklearn.linear_model import LogisticRegression
    clf_log = LogisticRegression()
    clf_log.fit(train_x_vector, train_y)
    y10 = clf_log.predict(test_x_vector[10])

    # Evaluation
    # mean accuracy
    svm_score = clf_svm.score(test_x_vector, test_y)
    dec_score = clf_dec.score(test_x_vector, test_y)
    gnb_score = clf_gnb.score(test_x_vector.toarray(), test_y)
    log_score = clf_log.score(test_x_vector, test_y)

    # F1 score

    print(data)


def demo_iris():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    print('demo_iris')


if __name__ == '__main__':
    demo_cls_nlp()
    # demo_iris()
