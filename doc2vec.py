import numpy as np
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from numpy.linalg import norm
from typing import List

# vector_size=100, window=5, min_count=1, workers=4


DEFAULT_PARAMS = dict(vector_size=99, window=5, min_count=1, workers=4)


class Doc2VecModel:
    """
    Doc2Vec maps documents, or a collection of words, to vectors in R^d space. The inverse distance between two vectors
    in this high-dimensional space gives us a concept of similarity between documents.

    Reference: https://radimrehurek.com/gensim/models/doc2vec.html
    """

    def __init__(self, params=DEFAULT_PARAMS):
        self.model = Doc2Vec(**params)

    def train_model(self, documents: List[str]):
        print("Training doc2vec model...", end=" ")
        word_tokens = [word_tokenize(r) for r in documents]
        documents = [TaggedDocument(r, [i]) for i, r in enumerate(word_tokens)]
        self.model.build_vocab(documents)
        self.model.train(documents, total_examples=len(documents), epochs=10)
        print("Done!\n")

    def to_vector(self, doc: str) -> np.ndarray:
        tokens = word_tokenize(doc)
        return self.model.infer_vector(tokens)

    def pairwise_similarity(self, doc: str, other_doc: str) -> float:
        distance = self.to_vector(doc) - self.to_vector(other_doc)
        return 1 / norm(distance)
