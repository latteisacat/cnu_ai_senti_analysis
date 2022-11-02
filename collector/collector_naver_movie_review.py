import requests
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
    print(f'제목: {title}')
    # 리뷰 수집 코드 작성
    review = []
    temp = []
    num = 243
    while True:
        url = f"https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={num}"
        # 네이버 영화는 마지막 페이지를 초과하는 페이지가 들어오면 마지막 페이지를 유지하게 된다.
        # 따라서 이전의 url에서 가져온 내용과 현재 temp에 저장된 내용의 동일성을 검사해야 같은 페이지임을 유추할 수 있다.
        # 함수 호출을 두 번씩 이나 하므로 좀 비효율적으로 보인다 다른 방법은 없을까?
        if temp == review_collector(url):
            break
        else:
            temp = review_collector(url)
        review = review + temp
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

