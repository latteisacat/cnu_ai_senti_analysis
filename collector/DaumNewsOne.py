# 1.프로젝트(cnu_ai_senti_analysis-main)
# ┖2.python package(collector)
#  ┖3.Python file(test.py, DaumNewsOne.py)
# - python package: python file들을 모아두는 폴더
#                           폴더아이콘안에 구멍 뚫려있음

# import와 Library(module)
# - Python 코드를 직접 작성해서 개발할 수도 있지만
# - 다른 개발자가 이미 만들어 놓은코드를 사용하면 편리함
# - 이미 개발되어있는 코드들의 묶음 = 라이브러리(module)
#   1.built in library: Python 설치 시 자동으로 제공 예: math, sys, os 등
#   2.외부 Library: 직접 추가해서 사용 ! 예 : requests, beautifulSoup4

# Library를 사용하기 위해서는 import 작업 진행
# - import는 도서관에서 필요한 책을 빌려오는 개념

import requests  # 책 전체를 빌려옴
from bs4 import BeautifulSoup  # bs4라는 책의 BeautifulSoup 1개 파트만 빌려옴

# 목표 : Daum 뉴스 웹페이지의 제목과 본문 데이터를 수집
# 1. url: https://v.daum.net/v/20221006083131071
url = 'https://v.daum.net/v/20221006083131071'
# 2. requests로 해당 url의 html 전체 코드를 수집

result = requests.get(url)
# print(result.text)

# 3. beautifulsoup 를 통해서 '제목과 본문'만 추출
doc = BeautifulSoup(result.text, 'html.parser')
title = doc.select('h3.tit_view')[0].get_text()
# python 은 []: List Type
# index 0  1  2  3  4
#      [5, 6, 7, 9, 10]:List 내에는 다양한 데이터 저장 가능


print(f'뉴스제목:{title}')
