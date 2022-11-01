# 프로그램 실행!
# 필요한 기능들을 호출해서 사용

from collector.collector_naver_movie_review import movie_review_crawler

movie_code = input("영화 코드를 입력하세요 : ")  # 네이버 영화 코드
movie_review_crawler(movie_code)
