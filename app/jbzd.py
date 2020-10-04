import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass(order=True)
class Meme:
    pluses: int
    url: str


def fetch_memes_page(page):
    page = requests.get(f"https://jbzd.com.pl/str/{page}")
    soup = BeautifulSoup(page.content, 'html.parser')

    articles = soup.select("article")
    article_objects = []

    for article in articles:
        image_nodes = article.select("div.article-content div.article-container div.article-image a img.article-image")
        # If post is not image post (video or something else) then ignore
        if not image_nodes:
            continue
        src = image_nodes[0].get('src', '')

        pluses_nodes = article.select("div.article-actions span.article-action vote")
        if not pluses_nodes:
            pluses = 0
        else:
            pluses = int(pluses_nodes[0].get(':score', '0'))

        meme = Meme(pluses, src)
        article_objects.append(meme)

    return article_objects


def _get_memes_until(url_limit=None, page_limit=20):
    all_memes = []
    for page in range(1, page_limit+1):
        page_memes = fetch_memes_page(page)
        for meme in page_memes:
            if url_limit and meme.url == url_limit:
                return all_memes
            all_memes.append(meme)
    return all_memes


def get_best_memes(count, url_limit=None, page_limit=20):
    memes = _get_memes_until(url_limit, page_limit)
    memes.sort(reverse=True)
    return memes[:count]


# print(fetch_memes_page(3))
print(get_best_memes(5))
