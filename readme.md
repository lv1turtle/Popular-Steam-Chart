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

- MySQL DB 연동
  - `popcat/setting.py`의 주석 제거 및 수정
    ```
    # default
    """
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    """

    # mysql
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "SteamChart",
            "USER": "root", # 본인 mysql user
            "PASSWORD": "", # 본인 mysql password
            "HOST": "127.0.0.1",
            "PORT": 3306,
        }
    }
    ```

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

- 프로젝트로 이동 & 서버 실행
    ```
    python manage.py runserver
    ```

