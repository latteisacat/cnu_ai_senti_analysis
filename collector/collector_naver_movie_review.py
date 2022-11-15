import requests
import re
import math
from bs4 import BeautifulSoup
from db.database import create_review


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

        for i, one in enumerate(review_list): # review 1건씩 수집 (MongoDB 에 저장할 예정)
            # 리뷰, 평점, 작성자, 작성일자
            score = one.select('div.star_score > em')[0].get_text()
            # review = one.select(f'#_filtered_ment_{i}')[0].get_text().strip() 이렇게 id로 찾는 방식은
            # id가 자주변경되는 데이터 중 하나라 좋은 방식이 아니라고 하심.
            review = one.select('div.score_reple > p > span')[-1].get_text().strip()  # -1은 마지막 인덱스

            # 날짜 시간 -> 날짜만 추출
            # 예: 2022.10.19 15:28 -> 2022.10.19
            # - 날짜는 항상 16글자로 구성
            # [3:] 3~끝까지
            original_date = one.select('div.score_reple > dl > dt > em')[-1].get_text()
            date = original_date[0:11]
            # 문자열 추출
            # [시작:끝+1], 끝은 포함 X
            # [:15] 0~14

            original_writer = one.select('div.score_reple > dl > dt > em')[0].get_text().strip()
            # writer = re.sub("(.)", "", original_writer)
            idx_end = original_writer.find('(')
            writer = original_writer[:idx_end]
            count += 1
            print(f"## 리뷰 -> {count} ####################################################################")
            print(f'# Review: {review}')
            print(f'# Score: {score}')
            print(f'# Writer: {writer}')
            print(f'# Date: {date}')
            # Review data 생성
            # -> 규격(포멧) -> JSON
            # JSON -> 데이터를 주고받을 때 많이 사용하는 타입
            # MongoDB -> BSON(Binary JSON) = JSON
            # python의 Dictionary = JSON
            #
            # Python의 dictionary 타입 = JSON = BSON
            # {Key:value, Key:value, Key:value}
            # dict type은 데이터를 꺼낼 때 key 값으로 꺼냄
            # List type 은 index 값으로 꺼냄
            data ={
                'title': title,
                'score': score,
                'review': review,
                'writer': writer,
                'date': date
            }
            create_review(data)

# 이후 할 일 수집(리뷰)-> 저장(MongoDB) -> 전처리, 탐색 -> 딥러닝 모델 학습&평가(긍정/부정 분석기)->시각화 또는 실제 데이터 서비스
# MongoDB 데이터베이스 사용 방식
# 1. Local(컴퓨터) 설치 - 노트북
# 2. 웹 클라우드 사용(ip, 내부 ip 사용X) - 컴퓨터
# https://github.com/ChoLong02/2022_02_cnu_ai 교수님 코드
# 저장 배우면서 이론 수업 진행되는데 여기서 기말 나옴

# Python코드  <- pymongo -> mongoDB