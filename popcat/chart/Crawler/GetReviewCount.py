from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
import time
import json


def GetReviewCount():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    actions = ActionChains(driver)

    # 100위 가져오기
    driver.get("https://store.steampowered.com/search/?os=win&filter=topsellers&ndl=1")
    driver.implicitly_wait(1)
    driver.find_element(By.XPATH, '//*[@id="additional_search_options"]/div[3]/div[1]').click()
    driver.implicitly_wait(1)
    driver.find_element(By.XPATH, '//*[@id="narrow_category1"]/div[1]/span').click()
    driver.implicitly_wait(3)
    # 리스트 개수 채우기위한 스크롤 아래로
    actions.send_keys(Keys.END).perform()
    driver.implicitly_wait(3)
    actions.send_keys(Keys.END).perform()
    # search_resultsRows 리스트 리뷰 검색을 위한 순위 리스트 100
    gameQueue = []
    for i in range(10):
        gameLink = (
            driver.find_element(By.ID, "search_resultsRows")
            .find_elements(By.TAG_NAME, "a")[i]
            .get_attribute("href")
            .split("/")
        )
        gameQueue.append([gameLink[4], gameLink[5]])

    # 리뷰수 가져오기
    # 스팀 리뷰수 그래프를 그리는 데이터 appreviewhistogram
    for i in range(len(gameQueue)):
        driver.get("https://store.steampowered.com/appreviewhistogram/{}".format(gameQueue[i][0]))
        time.sleep(3)
        json_data = driver.find_element(By.TAG_NAME, "pre").text
        data = json.loads(json_data)
        # print(gameQueue[i])
        if len(data["results"]["recent"]) > 1:
            gameQueue[i].append(data["results"]["recent"][-2]["recommendations_up"])
            gameQueue[i].append(data["results"]["recent"][-2]["recommendations_down"])
        else:
            gameQueue[i].append(0)
            gameQueue[i].append(0)
        print(gameQueue[i])
    # 가져온 데이터 출력
    return gameQueue
GetReviewCount()