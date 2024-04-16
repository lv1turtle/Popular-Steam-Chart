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

- MySQL DB 연동
  - `popcat/popcat/setting.py`의 주석 제거 및 수정
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

- 프로젝트로 이동 & 서버 실행
```
cd popcat
python manage.py runserver
```

