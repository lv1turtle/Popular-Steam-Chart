# Popular_Steam_Chart
We are developing Steam Trend Dashboard by tags for developers

## 프로젝트 소개

- 주제
  > 개발자를 위한 게임 태그별 Trend DashBoard
  
- 배경 및 목표
  > 디지털 게임 배포 플랫폼인 Steam 사이트 실시간 정보를 이용하여,
  > 
  > 개발자 관점에서 게임 개발에 필요한 사업성 정보, Trends 정보를 파악 

## 프로젝트 구현

### E-R Diagram
![image](https://github.com/lv1turtle/Popular_Steam_Chart/assets/32154881/01d95966-48d8-4b4c-8253-06ff8bd58e48)

### Selenium을 이용한 Web Crawling ( Steam - Top Sellers 100 )
>https://store.steampowered.com/charts/topselling/global

### Django - MySQL 연동, 데이터 전처리 및 적재
![image](https://github.com/lv1turtle/Popular_Steam_Chart/assets/32154881/17cac867-02b2-4ebe-bf30-f6852da5ef85)

### Chart - Highcharts with Django
![image](https://github.com/lv1turtle/Popular_Steam_Chart/assets/32154881/5de4db39-6cac-4485-8806-f581fd91ead0)
![image](https://github.com/lv1turtle/Popular_Steam_Chart/assets/32154881/5c0c11bb-a031-447b-ba17-e757c5b81dbc)

### Chart - Matplotlib
![image](https://github.com/lv1turtle/Popular_Steam_Chart/assets/32154881/bdacaa7f-a50a-4917-a767-08ddb0026388)

### Search for games by tag_list
![image](https://github.com/lv1turtle/Popular_Steam_Chart/assets/32154881/bf042597-f7e2-472a-8e9c-dcd33c1fe144)

### Main Page
![image](https://github.com/lv1turtle/Popular_Steam_Chart/assets/32154881/2c0201c3-2461-461b-bdc7-6343f9b0f7e2)


## 프로젝트 실행 방법

패키지 설치
- clone

- python 가상환경 생성
    ```
    py -m venv {venv_name}
    ```

- 가상환경 실행
    ```
    {venv_name}\Scripts\activate.bat
    ```

- 패키지 다운로드
    ```
    pip install -r requirements.txt
    ```

- popcat으로 이동
    `cd popcat`

- 프로젝트로 이동 & 서버 실행
    ```
    python manage.py runserver
    ```


## MySQL DB 연동
- `popcat/secret_settings.py`를 생성해서 user, pw 작성해주시면 됩니다.
    ```
    # mysql
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "SteamChart",
            "USER": "", # 본인 mysql user
            "PASSWORD": "", # 본인 mysql password
            "HOST": "127.0.0.1",
            "PORT": 3306,
        }
    }
    ```

    ( gitignore에 `secret_settings.py` 추가했으나 작동이 안되는 경우
    `git rm -r --cached`를 진행해서 캐시 삭제하고 add 해주세요. )

- MySQL 내 DB - SteamChart 생성
    - mysql 진입
    `mysql -u root -p`

    - DB 생성
    `CREATE DATABASE SteamChart CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;`

    - mysql 나오기
    `ctrl-z `

  - Migration을 통한 DB 테이블 생성
    `python manage.py migrate`

- MySQL Sample Data 삽입 ( 선택 사항 )

  - Sample data 생성
    - mysql 진입
    `mysql -u root -p`

    - DB 선택
    `use SteamChart;`

    - Sample Data insert
    `source sample.sql`

- DATABASE 리셋 ( 선택 사항 )
  - mysql 진입
    `mysql -u root -p`
    
  - DB 제거
    `drop database steamchart;`

  - mysql 나오기
      `ctrl-z `

  - Migration을 통한 DB 테이블 생성
      `python manage.py migrate`

- Crawl Data 받기
  - 서버 실행

    `python manage.py runserver`

  - crawling 실행
    `http://127.0.0.1:8000/test/`

