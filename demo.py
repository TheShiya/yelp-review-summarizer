from summarizer import Summarizer
from doc2vec import Doc2VecModel
from scrape import get_reviews


DEFAULT_URL = "https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2"


def main(url: str = DEFAULT_URL, max_pages: int = 3):
    print("* Multi-document Summarizer Demonstration *\n")
    reviews = get_reviews(url, max_pages=max_pages)
    summarizer = Summarizer(reviews, sim_metric="doc2vec")
    results = summarizer.summarize(budget=0.1)
    print('-----------------\nSample output reviews:\n')
    [print("{}: {}\n".format(i + 1, res)) for i, res in enumerate(results[:5])]


if __name__ == "__main__":
    main()
