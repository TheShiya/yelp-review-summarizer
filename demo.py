from summarizer import Summarizer
from doc2vec import Doc2VecModel
from scrape import get_reviews


DEFAULT_URL = 'https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2'


def main(url: str =DEFAULT_URL):
    print('* Multi-document Summarizer Demonstration *\n')
    reviews = get_reviews(url, max_pages=4)
    summarizer = Summarizer(reviews, sim_metric='doc2vec')
    results = summarizer.summarize(budget=0.1)
    (print('{}: {}\n'.format(i, results)) for i, res in enumerate(results))


if __name__ == '__main__':
    main()
