# mongodb 연결, 데이터 1건 저장 테스트
from pymongo import MongoClient
from database import create_review

create_review()

# 연결(Connection) 정보
#  - DB_HOST : mongodb에 접속할 IP + PORT
#  - DB_ID : mongodb 계정
#  - DB_PW : mongodb 암호

#               연결(IP + PORT)
#               ID & PW
# Python  --------------------------- MongoDB

# 127.0.0.1 = localhost: 로컬 ip
# port번호 기본적으로 프로그램 고유 포트번호
# ssh: 22
# http: 80
# mariadb: 3386
# mongodb: 27017
# client = MongoClient('127.0.0.1', 27017)

# DBMS: 데이터베이스 관리 시스템  ->  MongoDB
# DB(데이터베이스): 데이터 저장소  -> 다수의 DB(Shop, Blog)
# DB:Shop
#  - Collection(Table): 회원 정보
#  - Collection(Table): 상품 정보
#  - Collection(Table): 주문 정보
#  - Collection(Table): 게시글 정보

# DB: movie
#  ㄴ Collection: review
# db = client['movie']  # mongodb에 공간(db)생성
# collection = db.get_collection('review')
# data = {"msg": "MongoDB 데이터 테스트"}  # 데이터 1건 생성
# collection.insert_one(data)  # 1건의 데이터를 저장

