import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

HOST = "https://habr.com"
ARTICLES = f"{HOST}/ru/all/"


def wait_element(driver, delay_seconds=1, by=By.TAG_NAME, value=None):
    """
    Иногда элементы на странце не прогружаются сразу
    Функция ждет delay_seconds если элемент еще не прогрузился
    Если за отведенное время элемент не прогружается выбрасывается TimeoutException
    :param driver: driver
    :param delay_seconds: максимальное время ожижания
    :param by: поле поиска
    :param value: значение поиска
    :return: найденный элемент
    """

    return WebDriverWait(driver, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )


if __name__ == "__main__":
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(ARTICLES)

    articles_data = []

    articles_element = driver.find_element(By.CLASS_NAME, "tm-articles-list")
    for i, article_element in enumerate(
        articles_element.find_elements(By.TAG_NAME, "article"), start=1
    ):

        title_element = article_element.find_element(By.TAG_NAME, "h2")
        title = title_element.text

        link_element = title_element.find_element(By.TAG_NAME, "a")
        link = link_element.get_attribute("href")
        time_element = wait_element(
            driver,
            delay_seconds=20,
            by=By.XPATH,
            value=f"//div[@class='tm-articles-list']//article[{i}]//div//div//div//span[2]//time",
        )
        #  про XPATH https://www.guru99.com/xpath-selenium.html
        time = time_element.accessible_name
        articles_data.append({"title": title, "link": link, "time": time})

    for article_dict in articles_data:
        driver.get(article_dict["link"])
        try:
            wait_element(driver, 1, by=By.CLASS_NAME, value="tm-comment__body-content_v2")
        except TimeoutException:
            # если комментарии за 1 секунду не прогрузились, считаем, что их нет
            pass
        comment_elements = driver.find_elements(By.CLASS_NAME, "tm-comment__body-content_v2")

        comments_text = []
        for comment_element in comment_elements:
            comments_text.append(comment_element.text)
        article_dict["comments"] = comments_text

    print(articles_data)
    driver.quit()
