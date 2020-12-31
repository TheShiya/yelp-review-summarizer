# Yelp Review Summarizer

<p align="center">
<img src="banner.png" alt="art" width="630"/>
</p>

#### *Comes with an asynchronous review scraper!*

### Overview

These tools help you to scrape and summarizes Yelp reviews for any business! Works best if there are at least a few hundred reviews. Note: this is a spin-off from an academic research project: https://github.com/TheShiya/text-summarization-project/

### Usage

The following example scrapes 3 pages of reviews (60 reviews) from Omar's Mediterranean Cuisine. The summarizer uses doc2vec pairwise similarity between reviews, and the output reviews contains at most 500 characters.

```Python
url = "https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2"
n_pages = 2
budget = 500

scraper = YelpScraper(url)
reviews = scraper.scrape(n_pages)
summarizer = Summarizer(reviews, sim_metric="doc2vec")
results = summarizer.summarize(budget=budget)
```
### Sample output
```Python
1: just picked up food from them yesterday and couldn't be happier, a platter comes with two sides and a salad. also added pita and baklava. food was fresh and delicious, they fried the falafel right there. one of the best mediterranean cuisine in new york!

2: damn good. i was in the area for a hair salon appointment and almost missed this. the food is amazing. great quality, ingredients, very filling and delicious. i highly recommend!!!
```

### Content
* summarizer.py - contains the main summarization algorithm
* doc2vec.py - contains a doc2vec model that computes pairwise review similarity
* scraper.py - contains an asynchronous Yelp scraper that scrapes real reviews from any Yelp business page

### Reference
[Lin, Hui, and Jeff Bilmes. "Multi-document summarization via budgeted maximization of submodular functions." Human Language Technologies: The 2010 Annual Conference of the North American Chapter of the Association for Computational Linguistics. 2010.](https://www.aclweb.org/anthology/N10-1134.pdf)
