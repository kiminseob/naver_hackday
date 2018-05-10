2018 Campus Hackday :)
# hackday_crawler_search
[마크다운 문법](https://github.com/biospin/BigBio/blob/master/reference/%EB%A7%88%ED%81%AC%EB%8B%A4%EC%9A%B4.md)

## 개발환경
ubuntu 16.04.4 LTS
## 개발 언어
python 3.5.2
## 라이브러리
crawler : beautifulsoup 4.4.1  
database : sqlite3 3.11.0  
## Web application framework  
Django 2.0.5
## front-end component library
Bootstrap

***

# 진행상황 18.5.11
## 크롤러
뽐뿌 뉴스 항목(방송/연예/라이프/여행/IT/취업/스포츠/정치/경제)중 방송/연예 부분 테스트용 50개 기사 크롤링
## 검색 서비스
1. 수집 : 방송/연예 부분 기사 (to do : 나머지 기사 모두, 시간이 되면 이미지까지 수집해보자 )  
2. 정제 : 기사 제목, 기사 내용, 기사 업로드 날짜, 기사 ID  
3. 색인 : ( to do : 역인덱스 방법에 도전 )  
4. 검색 : 검색어를 추출 후, 공백을 기준으로 키워드를 구분함. 키워드가 기사의 제목 또는 내용과 일치하는 query가 있으면 해당 query를 합하여 queryset을 넘겨주어 웹에 출력
## view page
1. layout frame  
header : naver hacday logo, profile ,searchbar  
body : - (nothing)  
2. main view  
body : 네이버 핵데이에 관련된 동적인 텍스트를 보여줌  
3. search view  
div : 검색어에 해당하는 기사를 '기사제목&기사내용(15글자제한)'묶음의 div로 생성  
body : 생성된 div들을 집어넣음  
4. content view  
body-div : 검색된 기사를 클릭 시 이곳으로 넘어와 해당 기사의 전체 내용을 보여줌

***

# 개발 일기
**18.5.10**  
git 로컬 저장소를 새로 만들어 작업을 새로 시작했다.(git 사용법도 익힐겸)  
그동안 코딩했던 파일을 올리려고 push 했지만 잘 되지 않았다.  
구글링 결과 강제로 push 하는 방법을 알아내서 아래와 같은 명령어를 사용했으나  
'`'git push --force --set-upstream origin master'`'  
원격저장소의 내 브런치의 폴더 및 파일이 다 날라가고 그 위에 push된 내용이 새로 덮여 쓰여졌다.  
멘붕이 왔다. 그나마 아직 push한 작업이 적었고 혼자하는 작업이라 다행이었다.  
Readme만 다시 업뎃하면 될 것 같다. 다음부터는 저 명령어 쓰지 말자...

***

## 주제 선정 배경
* 검색 서비스의 수집, 정제, 색인, 검색의 단계를 아주 간단하게 경험 할 수 있는 기회입니다.
* 웹서버의 아파치 모듈과 검색결과를 보여주는 부분을 모두 경험할 수 있는 기회입니다.

## 요구사항(필수)
* 특정 웹사이트의 게시글 및 내용을 크롤링하는 크롤러 개발 (언어 제한X, 라이브러리 사용 가능)
* 크롤러와 아파치 모듈(C, C++)과 연동하여 크롤링 내용중 필요한 부분을 반환
* 웹브라우저를 통해 크롤링 내용중 일부를 검색 하여 결과 확인(RESTful/JSON)

## 요구사항(선택)
* 사용자 편의를 생각하는 검색
* 보기 좋은 결과 (라이브러리 사용 가능, 언어 제한X)
* 빠른 검색
* 빠른 반영
## 개발언어
C/C++: 아파치 모듈
웹페이지 및 크롤러는 제한 없음

## 플랫폼 
Linux + 아파치

## 기타 사항
개인별로 과제를 수행합니다.
