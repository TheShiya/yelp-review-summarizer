from typing import List
from nltk.tokenize import word_tokenize
from doc2vec import Doc2VecModel
import numpy as np
import heapq
import time


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

    An abstractive summarizer that uses a lazy greedy algorithm with a max heap to efficiently find the most
    semantically representative documents from a large corpus of documents.


    References:

    1. Lin, Hui, and Jeff Bilmes. "Multi-document summarization via budgeted maximization of submodular functions."
    Human Language Technologies: The 2010 Annual Conference of the North American Chapter of the Association for
    Computational Linguistics. 2010.

    2. homes.cs.washington.edu/~marcotcr/blog/
    """
    def __init__(
        self,
        documents: List[str],
        url: str = "",
        sim_metric: str = "jaccard",
        budget: float = 0.1,
    ):
        self.url = url
        self.documents = documents

        # Accepts budget as a percentage of total cost
        if 0 < budget < 1:
            self.budget = int(budget * sum(cost_func(x) for x in documents))
        else:
            self.budget = budget

        if sim_metric == "doc2vec":
            print("Initializing and training gensim Doc2Vec...", end=" ")
            d2v = Doc2VecModel().train_model(documents)
            print("Done.")
            self.sim_func = d2v.similarity
        elif sim_metric == "jaccard":
            self.sim_func = jaccard_index
        else:
            assert sim_metric in ["doc2vec", "jaccard"]

    def _compute_pairwise_similarities(self):
        n = len(self.documents)
        sim_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i, n):
                sim = self.sim_func(self.documents[i], self.documents[j])
                sim_matrix[i, j] = sim
                sim_matrix[j, i] = sim
        return sim_matrix

    def summarize(self, r=0.3, lambda_=1):
        def _gain(item, f, o, c):
            return (f(o.union({item})) - f(o)) / c[item] ** r

        def _f(s):
            cut = sum(sim[i, j] for i in (set(docs) - set(s)) for j in set(s))
            redundancy = sum(
                [sum([sim[i, j] for i in (set(s) - set({j}))]) for j in set(s)]
            )
            return cut - lambda_ * redundancy

        start = time.time()
        print("Starting summarization...", end=" ")
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
                sum([costs[i] for i in output]) + costs[k] <= self.budget
                and _gain(k, _f, output, costs) >= 0
            ):
                output = output.union({k})
            candidates.remove(k)

        v_star = sorted(
            [d for d in docs if costs[d] <= self.budget], key=lambda d: _f({d})
        )[-1]
        if _f({v_star}) >= _f(output):
            output = {v_star}

        print("Done. Took {:.1f}s.".format(time.time() - start))
        return [self.documents[doc] for doc in output]
