import requests
import re
import math
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
    url = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=1"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    all_count = doc.select('strong.total > em')[0].get_text() #리뷰 전체 수 수집
    # "2,480" : str type(문자열), 문자 ','가 포함되어 있어 int 형으로 변환이 불가
    numbers = re.sub(r"[^0-9]", "", all_count)  # 0부터 9 제외 전부 공백으로 변환 re는 정규식 함수 파이썬 정규식 검색해보자.
    pages = math.ceil(int(numbers)/10)
    print(f'The total number of pages to collect is {pages}')

    # 해당 페이지 리뷰 수집!
    count = 0 # 전체 리뷰 수를 count
    for page in range(1, pages + 1):
        url = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}"
        result = requests.get(url)
        doc = BeautifulSoup(result.text, 'html.parser');
        review_list = doc.select('div.score_result > ul >li')  # 1page의 리뷰 10건
        print(review_list)

        for i, one in enumerate(review_list): # review 1건씩 수집
            # 리뷰, 평점, 작성자, 작성일자
            score = one.select('div.star_score > em')[0].get_text()
            # review = one.select(f'#_filtered_ment_{i}')[0].get_text().strip()
            review = one.select('div.score_reple > p > span')[-1].get_text().strip()  # -1은 마지막 인덱스
            print(f'# Score : {score}')
            print(f'# Review : {review}')
        break

