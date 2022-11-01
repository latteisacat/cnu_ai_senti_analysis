import requests
from bs4 import BeautifulSoup
from collector.practice.CollectorService import get_daum_news
# 1페이지에서 15개의 뉴스(제목, 본문) 수집 코드
# -> 1~마지막 페이지 까지 돌면서 수집하도록 수정

# https://news.daum.net/breakingnews/digital?page=3
# 쿼리스트링(QueryString): url(주소) + data
# url ? data

# range(시작값, 끝값, 크기)
# - 크기는 생략가능(default 1)
# - 끝값은 끝값 -1 까지
# -> range(1, 3, 1) = [1, 2]
# -> range(1, 10, 2) = [1, 3, 5, 7, 9]
news_count = 0
num = 1
headers = {'class': "os_windows chrome pc version_106_0_0_0 "}
while True:
    print(f'\n----------------------{num} page----------------------\n')
    main_url = f'https://news.daum.net/breakingnews/digital?page={num}'  # 1page

    result = requests.get(main_url, headers=headers)

    doc = BeautifulSoup(result.text, 'html.parser')

    url_list = doc.select('ul.list_news2 a.link_txt')
    if len(url_list) == 0:
        break

    else:
        for i, url in enumerate(url_list):
            print(f'인덱스:{i+1}, url: {url["href"]}')
            get_daum_news(url["href"])
            news_count += 1
        num += 1

print(f'''
------------------------------------
총 {news_count}개의 뉴스를 수집하였습니다.
------------------------------------''')