from bs4 import BeautifulSoup
from typing import List
import requests
import asyncio
import aiohttp
import ssl
import re


class YelpScraper:
    """
    Usage:
    url = "https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2"
    ys = YelperScraper(url, n_pages=2)
    reviews = ys.scrape()
    """
    def __init__(self, url: str, n_pages: int):
        self.url = url
        self.n_pages = n_pages
        self.reviews = []

    @staticmethod
    def _clean_review(review: str) -> str:
        """
        replace and remove certain characters in Yelp reviews
        """
        review = re.sub("(&amp;#39;)+", "'", review)
        review = re.sub("(<br&gt;)+", " ", review)
        review = re.sub("\xa0", "", review)
        review = review.lower()
        return review

    @staticmethod
    def _parse_html(html: str) -> List[str]:
        soup = BeautifulSoup(html, features="lxml")
        script_sections = soup.findAll("script")
        regex = re.compile("maps.googleapis.com.*Write a Review")
        reviews_section = str([s for s in script_sections if regex.search(str(s))][0])
        reviews_section = re.search("<!--(.*)-->", reviews_section).group(1)
        reviews_section = re.sub("null", "None", reviews_section)
        reviews_section = re.sub("false", "False", reviews_section)
        reviews_section = re.sub("true", "True", reviews_section)
        reviews_dict = eval(reviews_section)
        reviews = reviews_dict["bizDetailsPageProps"]["reviewFeedQueryProps"]["reviews"]
        reviews = [r["comment"]["text"] for r in reviews]
        reviews = [YelpScraper._clean_review(r) for r in reviews]
        return reviews

    @staticmethod
    async def _fetch(session, url):
        """
        Asynchronous function to retrieve HTML
        """
        async with session.get(url) as response:
            assert response.status == 200
            html = await response.text()
            return html

    async def scrape_func(self) -> List[str]:
        urls = [self.url]
        urls += [self.url + "?start=" + str(i * 20) for i in range(1, self.n_pages)]
        self.reviews = []
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                tasks.append(self._fetch(session, url))
            html_list = await asyncio.gather(*tasks)
            for html in html_list:
                self.reviews += self._parse_html(html)

    def scrape(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.scrape_func())
        return self.reviews


url = "https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2"
ys = YelpScraper(url, n_pages=2)
reviews = ys.scrape()

print(reviews)
