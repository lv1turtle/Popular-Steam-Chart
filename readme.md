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

- 서버 실행
```
python manage.py runserver
```

- secret_setting.py
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

SECRET_KEY = {
    # django settings.py SECRET_KEY 입력하시면 됩니다.
}