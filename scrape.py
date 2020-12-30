from bs4 import BeautifulSoup
from typing import List
import requests
import asyncio
import aiohttp
import ssl
import re


SSLContext = ssl.SSLContext


def clean_review(t: str) -> str:
    """
    replace and remove certain characters in Yelp reviews
    """
    t = re.sub("(&amp;#39;)+", "'", t)
    t = re.sub("(<br&gt;)+", " ", t)
    t = re.sub("\xa0", "", t)
    t = t.lower()
    return t


async def get_reviews(url: str) -> List[str]:
    """
    Scrapes and cleans users review from Yelp.com. Example:

    url = 'https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2'
    reviews = get_reviews(url, max_pages=4)

    :param url: url to the Yelp page
    :return: list of review strings
    """

    response = await aiohttp.request('GET', url)
    body = await response.read_and_close(decode=True)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
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
    reviews = [clean_review(r) for r in reviews]
    return reviews


def get_reviews(url: str, max_pages: int = 2) -> List[str]:
    """
    Scrapes and cleans users review from Yelp.com.

    Example usage:
    url = 'https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2'
    reviews = get_reviews(url, max_pages=4)

    :param url: url to the business page, e.g. "https://www.yelp.com/biz/china-jade-new-york-2"
    :param max_pages: maximum number of pages to scrape (20 reviews per page as of 12/28/2020)
    :return: list of review strings
    """
    print("Scraping {} pages of reviews from:\n{}".format(max_pages, url))
    reviews_all = []
    for i in range(0, max_pages):
        curr_url = "{} ?start={}".format(url, i * 20) if i > 0 else url
        response = requests.get(curr_url)
        soup = BeautifulSoup(response.text, features="lxml")
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
        reviews = [clean_review(r) for r in reviews]
        reviews_all += reviews
    print("Downloaded {} reviews\n".format(len(reviews_all)))
    return reviews_all


async def fetch(session, url):
    async with session.get(url) as response:
        assert response.status == 200
        html = await response.text()
        print(html[:100])


async def main():
    urls = [
        "https://www.yelp.com/biz/omars-mediterranean-cuisine-new-york-2",
        "https://www.yelp.com/biz_photos/china-jade-new-york-2"
            ]
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        for html in htmls:
            print(html[:100])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())