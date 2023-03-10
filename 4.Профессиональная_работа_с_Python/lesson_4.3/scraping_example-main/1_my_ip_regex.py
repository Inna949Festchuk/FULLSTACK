import re

import requests

HOST = "https://2ip.ru/"

IP_REGEX = re.compile(r'<div.*?id="d_clip_button".*>\s*<span>(.*?)</span>')


def get_ip():
    html = requests.get(HOST).text
    return IP_REGEX.search(html).group(1)


if __name__ == "__main__":
    print(get_ip())
