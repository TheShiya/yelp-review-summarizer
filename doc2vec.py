from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from numpy.linalg import norm

# vector_size=100, window=5, min_count=1, workers=4


DEFAULT_PARAMS = dict(vector_size=99, window=5, min_count=1, workers=4)


class Doc2VecModel:
    def __init__(self, params=DEFAULT_PARAMS):
        self.model = Doc2Vec(**params)

    def train_model(self, documents):
        word_tokens = [word_tokenize(r) for r in documents]
        documents = [TaggedDocument(r, [i]) for i, r in enumerate(word_tokens)]
        self.model.build_vocab(documents)
        self.model.train(documents, total_examples=len(documents), epochs=10)
        return self

    def similarity(self, doc, other_doc):
        tokens = word_tokenize(doc)
        other_tokens = word_tokenize(other_doc)
        return norm(
            self.model.infer_vector(tokens) - self.model.infer_vector(other_tokens)
        )
