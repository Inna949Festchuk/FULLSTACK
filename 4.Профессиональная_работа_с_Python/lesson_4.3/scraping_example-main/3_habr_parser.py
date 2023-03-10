import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

HOST = "https://habr.com"
ARTICLES = f"{HOST}/ru/all/"


def get_headers():
    return Headers(browser="firefox", os="win").generate()


def get_text(url):
    return requests.get(url, headers=get_headers()).text


def parse_article(article_tag):
    link_tag = article_tag.find("a", class_="tm-article-snippet__title-link")
    if link_tag is None:
        return
    link = link_tag["href"]
    link = f"{HOST}{link}"
    return {
        "date": article_tag.find("time")["title"],
        "link": link,
        "title": link_tag.find("span").text,
    }


def parse_page(page):
    html = get_text(f"{ARTICLES}page{page}")
    soup = BeautifulSoup(html, features="html5lib")
    articles = soup.find(class_="tm-articles-list").find_all("article")
    articles_parsed = []
    for article in articles:
        parsed = parse_article(article)
        articles_parsed.append(parsed)
    return articles_parsed


if __name__ == "__main__":
    for page in range(1, 51):
        print(page)
        print(parse_page(page))
