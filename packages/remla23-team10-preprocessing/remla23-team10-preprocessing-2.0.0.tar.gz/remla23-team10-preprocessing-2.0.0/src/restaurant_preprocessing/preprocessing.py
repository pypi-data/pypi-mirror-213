"""This module preprocesses the data"""
import pickle
import re
from urllib.request import urlopen

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')

class Preprocessing:
    """This class preprocesses the data"""

    def __init__(self):
        """Initialize the preprocessing module"""
        self.porter_stemmer = PorterStemmer()
        self.count_vectorizer = None
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')

        self.stopwords = all_stopwords


    def preprocess_dataset(self, dataset):
        """Preprocess the entire dataset"""
        corpus = []

        for i in range(0, dataset.shape[0]):
            corpus.append(self.preprocess_review(dataset['Review'][i]))
        return corpus

    def preprocess_review(self, review):
        """Preprocess a single review"""
        review = re.sub('[^a-zA-Z]', ' ', review)
        review = review.lower()
        review = review.split()
        review = [self.porter_stemmer.stem(word) for word in review \
                  if not word in set(self.stopwords)]
        review = ' '.join(review)
        return review

    def fit_transform(self, corpus):
        """Fit a corpus and transform it into a BoW representation"""
        self.count_vectorizer = CountVectorizer(max_features = 1420)
        return self.count_vectorizer.fit_transform(corpus).toarray()

    def transform(self, corpus):
        """Transform a corpus into a BoW representation"""
        if self.count_vectorizer is None:
            raise Exception("Vectorizer is not initialized. \
            Please call fit_transform or load from PKL or URL first.")
        return self.count_vectorizer.transform(corpus).toarray()

    def vectorizer_from_pkl(self, cv_file):
        """Load the vectorizer from a PKL file"""
        with open(cv_file, "rb") as file:
            self.count_vectorizer = pickle.load(file)

    def vectorizer_from_url(self, url):
        """Load the vectorizer from a URL"""
        with urlopen(url) as file:
            self.count_vectorizer = pickle.load(file)

    def save_vectorizer(self, filename):
        """Save the vectorizer to a file"""
        with open(filename, "wb") as file:
            pickle.dump(self.count_vectorizer, file)