from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


links = []
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.get("https://store.steampowered.com/charts/topselling/global")
    driver.implicitly_wait(10)
    for i in range(1,101):
        link = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="page_root"]/div[3]/div/div/div/div[3]/table/tbody/tr[{}]/td[3]/a'.format(i))))
        links.append(link.get_attribute("href"))

tag_list = {}
game_tag = {}
user_agent = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

for link in tqdm(links):
    res = requests.get(link, user_agent)        #인증을 피하기 위해 BeautifulSoup 사용
    soup = BeautifulSoup(res.text, "html.parser")
    tags = soup.find_all("a", "app_tag")
    if soup.find("div", id = "appHubAppName"):  #SteamDeck처럼 순위권에 있지만 게임 태그가 없는 것들 제외
        for tag in tags:
            tag = tag.text.strip()
            tag_list[tag] = tag_list.get(tag, 0) + 1
            game_name = soup.find("div", id = "appHubAppName").text
            game_tag[game_name] = game_tag.get(game_name, []) + [tag]

print(tag_list["FPS"])
print(game_tag["Counter-Strike 2"])


