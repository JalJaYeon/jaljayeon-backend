# 자연? 잘자연~

## 프로젝트 소개

2021 선린톤 대주제 '세계', 소주제 '자연' 의 주제에 대한 개발물입니다!

잘 "자연" 할 수 있도록 도와줌 ^^

## 기술 스택

-   Language: Python3
-   Framework: Django
-   Infra: AWS, Docker, Docker Compose
-   Database: PostgreSQL

## 프로젝트 실행 - 파이썬

### 필요한 것들

-   Python 3.9.5

### 필요한 패키지 설치

진행에 앞서, 다음의 명령어를 이용해 파이썬 가상환경을 만드는것을 추천합니다.  
다음의 명령어는 가상환경을 생성하고, 가상환경 안으로 들어가 pip를 최신버전으로 업그레이드 하는 내용입니다.

```sh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

다음의 명령어로 필요한 패키지들을 설치하세요.

```sh
pip install -r requirements.txt
```

### 개발 서버 실행

configs/envs.py 에서 필요한 설정들을 적절히 수정해주세요.

다음의 명령어로 개발 서버를 실행 할 수 있습니다.

```sh
python3 manage.py runserver
```

### 프로덕션 서버 실행

다음의 명령어로 8000번 포트에 gunicorn을 사용해 프로덕션 서버를 실행 할 수 있습니다.

```sh
gunicorn -b 0.0.0.0:8000 jaljayeon_backend.wsgi:application
```

혹은 UNIX 소켓을 사용해 서버를 실행 할 수 있습니다.

```sh
gunicorn -b unix:/tmp/gunicorn.sock jaljayeon_backend.wsgi:application
```
