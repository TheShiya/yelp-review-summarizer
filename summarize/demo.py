from summarize.scraper import YelpScraper
from summarize.summarizer import Summarizer

"""
A simple demonstration of the YelpScraper and Summarizer objects
"""

if __name__ == "__main__":
    print("* Multi-document Summarizer Demonstration *\n")

    url = "https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2"
    n_pages = 2
    budget = 500

    scraper = YelpScraper(url)
    reviews = scraper.scrape(n_pages)
    summarizer = Summarizer(reviews, sim_metric="doc2vec")
    results = summarizer.summarize(budget=budget)

    print("-----------------\nSample output reviews:\n")
    [print("{}: {}\n".format(i + 1, res)) for i, res in enumerate(results[:3])]
