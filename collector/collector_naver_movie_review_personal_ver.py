import requests
import re
from bs4 import BeautifulSoup


#################
# 1.영화 제목 수집 #
#################

# movie_code: 네이버 영화 코드(6자리 숫자)

# 제목 수집
# 함수
# 1. 생성 2. 호출
# - 함수는 생성하면 아무동작도 하지 않음
# - 반드시 생성 후 호출을 통해서 사용
# class
# log 공부
def movie_title_crawler(movie_code):
    url = f'https://movie.naver.com/movie/bi/mi/point.naver?code={movie_code}'
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    title = doc.select('h3.h_movie > a')[0].get_text()
    return title


# 리뷰 수집(리뷰, 평점, 작성자, 작성일자) + 제목
def movie_review_crawler(movie_code):
    title = movie_title_crawler(movie_code)  # 제목 수집
    print(f'>> Start collecting movies for {title}')
    # 리뷰 수집 코드 작성
    review = []
    num = 247
    url = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={num}"
    max = max_num(url)
    while num <= max:
        url = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={num}"
        review = review + review_collector(url)
        num = num + 1
    print(review)


def review_collector(url):
    result = requests.get(url)
    review = []
    doc = BeautifulSoup(result.text, 'html.parser')
    for i in range(0, 10):
        if len(doc.select(f'#_filtered_ment_{i}')) == 0:
            break
        review.append(doc.select(f'#_filtered_ment_{i}')[0].get_text().strip())
    return review


def max_num(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    num = doc.select('strong.total > em')[0].get_text()
    num = re.sub(r"[^0-9]", "", num)
    num = int((int(num) - 1)/10 + 1)
    return num
