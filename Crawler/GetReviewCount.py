from selenium import webdriver      
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
actions = ActionChains(driver)

driver.get("https://store.steampowered.com/search/?filter=topsellers&os=win")
driver.implicitly_wait(5)
# 리스트 개수 채우기위한 스크롤 아래로
actions.send_keys(Keys.END).perform()

# search_resultsRows 리스트 리뷰 검색을 위한 순위 리스트 100
gameQueue = []
for i in range(100):
    gameLink = driver.find_element(By.ID, "search_resultsRows").find_elements(By.TAG_NAME, "a")[i].get_attribute("href").split("/")
    gameQueue.append([gameLink[4], gameLink[5]])

driver.get("https://steamspy.com/login/")
driver.implicitly_wait(3)
id_input = driver.find_element(By.NAME,"username")
pw_input = driver.find_element(By.NAME,"password")
login_button = driver.find_element(By.NAME,"submit")


# 아이디 비밀번호 입력
ActionChains(driver).send_keys_to_element(id_input, "dkswodud0531").perform()
time.sleep(0.5)
ActionChains(driver).send_keys_to_element(pw_input, "Qwer1234").perform()
time.sleep(0.5)
# reCaptcha 처리
driver.find_element(By.CSS_SELECTOR, ".g-recaptcha div iframe").click()
time.sleep(0.5)
# 로그인 버튼
ActionChains(driver).click(login_button).perform()
# 홈페이지 이동
driver.get("https://steamspy.com")

# 임시로 1에서 5순위의 리뷰개수만 가져오는중 5 대신 len(gameQueue)넣으면 전체 가져올수있음
for i in range(5):
    driver.get("https://steamspy.com/app/{}".format(gameQueue[i][0]))
    driver.implicitly_wait(5)
    driver.find_element(By.ID, "tabs-nvd3").find_element(By.CSS_SELECTOR, "a[href='#tab-reviews']").click()
    time.sleep(3)
    js_data = driver.execute_script("return document.getElementById('tab-reviews').getElementsByTagName('script')[0].textContent;")
    json_data = json.loads(js_data.split('=', 1)[1].strip().strip(';'))
    today_review = int(json_data[0]["values"][-1][1]) + abs(int(json_data[1]["values"][-1][1]))
    gameQueue[i].append(today_review)
# 가져온 데이터 출력
print(gameQueue)