import requests
from bs4 import BeautifulSoup

HOST = "https://2ip.ru/"


def get_ip():
    html = requests.get(HOST).text
    soup = BeautifulSoup(html, features="html5lib")
    d_clip_button = soup.find(id="d_clip_button")
    snap_ip = d_clip_button.find("span")
    return snap_ip.text


if __name__ == "__main__":
    print(get_ip())
