import heapq
import time
from typing import List

import numpy as np
from nltk.tokenize import word_tokenize

from summarize.doc2vec import Doc2VecModel


def jaccard_index(s: str, t: str) -> float:
    """
    Implements word-wise Jaccard index (size of intersection / size of union)
    :param s: one string
    :param t: another string
    :return: Jaccard index, a float in [0, 1]
    """
    s_words = set(word_tokenize(s))
    t_words = set(word_tokenize(t))
    intersection = s_words.intersection(t_words)
    union = s_words.union(t_words)
    return len(intersection) / len(union)


def cost_func(document: str) -> int:
    return len(document)


class Summarizer:
    """
    Overview:
    An extractive summarize that uses a lazy greedy algorithm with a max heap to efficiently find the most
    semantically representative documents from a large corpus of documents.

    Example usage:
    summarize = Summarizer(['hi there', 'hello how are you'], sim_metric='doc2vec')
    res = summarize.summarize(budget=0.1)  # returns document no longer than 10% of total length

    References:
    1. Lin, Hui, and Jeff Bilmes. "Multi-document summarization via budgeted maximization of submodular functions."
    Human Language Technologies: The 2010 Annual Conference of the North American Chapter of the Association for
    Computational Linguistics. 2010.
    2. homes.cs.washington.edu/~marcotcr/blog/
    """

    def __init__(self, documents: List[str], sim_metric: str = "jaccard"):
        """
        :param documents: list of cleaned text documents
        :param sim_metric: similarity metric, currently available: "jaccard", "doc2vec"
        """
        self.documents = documents

        # Gensim's doc2vec will be significant slower and more interesting than jaccard
        if sim_metric == "doc2vec":
            d2v = Doc2VecModel()
            d2v.train_model(documents)
            self.sim_func = d2v.pairwise_similarity
        elif sim_metric == "jaccard":
            self.sim_func = jaccard_index
        else:
            assert sim_metric in ["doc2vec", "jaccard"]

    def _compute_pairwise_similarities(self) -> np.ndarray:
        """
        Computes pairwise document similarity using the specified similarity metric
        :return: n x n numpy array, where n is the number of documents
        """
        n = len(self.documents)
        sim_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i, n):
                sim = self.sim_func(self.documents[i], self.documents[j])
                sim_matrix[i, j] = sim
                sim_matrix[j, i] = sim
        return sim_matrix

    def summarize(self, budget, r: float = 0.3, lambda_: float = 1.0) -> List[str]:
        """
        Lazy greedy algorithm, refer to reference 1.
        :param lambda_: weight for redundancy; another component is representativeness)
        :param r: scaling factor for cost; higher r favors less costly documents
        :return: list of document strings
        """

        # Accepts budget as a percentage of total cost
        if 0 < budget < 1:
            budget = int(budget * sum(cost_func(x) for x in self.documents))
        else:
            budget = budget
        print("Settings: budget={}, r={}, lambda={}".format(budget, r, lambda_))

        # Computes gain in objective function with new addition
        def _gain(item, f, o, c):
            return (f(o.union({item})) - f(o)) / c[item] ** r

        # Computes sum of cut (representativeness) and weighted redundacy
        def _f(s):
            cut = sum(sim[i, j] for i in (set(docs) - set(s)) for j in set(s))
            red = sum([sum([sim[i, j] for i in (set(s) - {j})]) for j in set(s)])
            return cut - lambda_ * red

        print("Starting summarization...")
        start = time.time()

        n = len(self.documents)
        sim = self._compute_pairwise_similarities()
        docs = list(range(n))
        candidates = list(range(n))
        output = set({})

        costs = {i: cost_func(review) for i, review in enumerate(self.documents)}
        heap = [(-_gain(x, _f, output, costs), x) for x in candidates]
        heapq.heapify(heap)

        while candidates:
            k = None
            while k is None:
                prev_gain, head = heapq.heappop(heap)
                head_gain = -_gain(head, _f, output, costs)
                if len(heap) == 0 or head_gain <= heapq.nsmallest(1, heap)[0][0]:
                    k = head
                else:
                    heapq.heappush(heap, (head_gain, head))
            if (
                sum([costs[i] for i in output]) + costs[k] <= budget
                and _gain(k, _f, output, costs) >= 0
            ):
                output = output.union({k})
            candidates.remove(k)

        v_star = max([d for d in docs if costs[d] <= budget], key=lambda d: _f({d}))
        if _f({v_star}) >= _f(output):
            output = {v_star}

        print("Done. Took {:.1f}s.\n".format(time.time() - start))
        return [self.documents[doc] for doc in output]
