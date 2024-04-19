from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys, ActionChains
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm


def TopSeller():
    links = []
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get(
            "https://store.steampowered.com/search/?os=win&filter=topsellers&ndl=1"
        )
        actions = ActionChains(driver)
        driver.implicitly_wait(10)
        actions.send_keys(Keys.END).perform()
        driver.implicitly_wait(3)
        actions.send_keys(Keys.END).perform()
        for i in tqdm(range(1, 101)):
            link = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="search_resultsRows"]/a[{}]'.format(i))
                )
            )
            links.append(link.get_attribute("href"))

    game_data_list = []
    p_id = r'\d+'
    p_price = re.compile('Free|Try|Demo')
    p = re.compile("Free|Try|Demo")  # 무료 혹은 데모의 경우 잡아내기
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }

    for link in tqdm(links):
        res = requests.get(link, user_agent)
        soup = BeautifulSoup(
            res.text, "html.parser"
        )  # 인증 피하기 위해 BeautifulSoup 사용
        tags = soup.find_all("a", "app_tag")
        if soup.find("div", id="appHubAppName"):
            game_name = soup.find("div", id="appHubAppName").text
            game_id = int(re.search(p_id, link).group())
            if soup.find("div", "game_purchase_price price"):  # 가격 알아내기
                price = (
                    soup.find("div", "game_purchase_price price")
                    .text.strip()
                    .replace(",", "")
                    .replace("₩", "")
                )
            elif soup.find(
                "div", "discount_final_price"
            ):  # 할인중일 경우 할인 가격으로 알아내기
                price = (
                    soup.find("div", "discount_final_price")
                    .text.strip()
                    .replace(",", "")
                    .replace("₩", "")
                )
            if p_price.search(price):  # 무료 혹은 데모의 경우 가격 0으로 설정
                price = 0
            tags_list = [tag.text.strip() for tag in tags]
            game_data_list.append([game_name, tags_list, price, game_id])

    return game_data_list
