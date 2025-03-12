# MyDocker
# Project : MyDocker
Django-DRF를 이용한 간단한 커뮤니티 사이트를 가상 테스트해서 실시간 분석

## Project Introduction
- 간단한 CRUD 기능을 다수의 가상 테스트 유저를 만들어 기능 테스트
- 인원, 요청 간격, 요청 수 등을 조절하여 응답 시간 및 실패율 분석
- 스크래핑 및 시각화 도구를 활용하여 정밀 분석

## Development time
2025.01 ~ 2025.03

## Development Environment
- Programming Language : Python 3.10.14
- Framework : DJANGO, DJANGO-DRF
- Database : SQLite, Prometheus DB
- Deployment : Docker-compose
- Test Tools : Locust(2.33), Prometheus(2.3.1), Grafana 

## Installation
1. 깃허브 클론
```
https://github.com/Jingood/MyDocker.git
```
2. docker 실행
```
docker-compose build
docker-compose up
```
3. Django migration 진행
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```


## API Documentation
<https://devjingood.tistory.com/17>

## Apps Description
### 1. accounts
- JWT을 이용한 로그인 및 로그아웃, 회원가입
- 비밀번호 변경, 회원 탈퇴
### 2. posts
- 게시물 생성, 조회, 수정, 삭제, 좋아요
- 댓글 및 대댓글 생성, 수정, 삭제, 좋아요

## ERD
![Image](https://github.com/user-attachments/assets/9c87fcd3-00d8-417b-9c2b-28d9cce2e6a2)
