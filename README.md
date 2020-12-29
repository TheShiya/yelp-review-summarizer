# Yelp Review Summarizer

This is an extension of an academic research project: https://github.com/TheShiya/text-summarization-project/


#### Overview

These tools help you to scrape and summarizes Yelp reviews for any business! Works best if there are at least a few hundred reviews.

#### Usage

The following example scrapes 3 pages of reviews (60 reviews) from Omar's Mediterranean Cuisine. The summarizer will use doc2vec-based pairwise similarity between reviews, and the output will contain reviews with at most 500 characters in total.

```Python
url = "https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2"
max_pages = 3
budget = 500

reviews = get_reviews(url, max_pages=max_pages)
summarizer = Summarizer(reviews, sim_metric="doc2vec")
results = summarizer.summarize(budget=budget)
```
Sample output:
```Python
Sample output reviews:

1: omar? more like o man. love their stuff. my go-to is the chicken platter with falafel and eggplant salad. the eggplant salad is literally so so delicious, especially if you dip the pita bread in it. they make the falafels fresh (as in when you order, they scoop some of the falafel mix into the deep fryer). the portion is huge so you can split it up into two meals if you want, and they also give you a free baklava with every takeout order! i love baklava's and this tiny dessert after a delish meal is the perfect finishing touch.

2: i ordered the shawarma platter with some baba ganoush and mediterranean rice. it came with a side of baklava and lots of nice sauces (garlic, hot sauce). the food was yummy and the service was great. i def plan on reordering!

3: i came here during lunch hours. i have had better mediterranean food elsewhere. for instance in long island city, and in queens. the food in here is acceptable, but imo not worth for the price. perhaps because it is located in manhattan. i liked the dessert. it was fresh, tasty, and crunchy
```

Reference: [Bilmes & Lin (2010)](https://www.aclweb.org/anthology/N10-1134.pdf)
