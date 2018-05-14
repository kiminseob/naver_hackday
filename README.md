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

# 진행상황 18.5.13
## 크롤러
뽐뿌 뉴스 항목(방송/연예, 라이프/여행, IT/취업, 스포츠, 정치/경제)중 방송/연예 부분 테스트용 50개 기사 크롤링
## 검색 서비스
1. 수집 : 방송/연예 부분 기사 (to do : 나머지도 )  
2. 정제 : 기사 제목, 기사 내용, 기사 업로드 날짜, 기사 ID  
3. 색인 : ( to do : 역인덱스 방법에 도전 )  
4. 검색 : 검색어를 추출 후, 공백을 기준으로 키워드를 구분함. 키워드가 기사의 제목 또는 내용과 일치하는 query가 있으면 해당 query를 합하여 queryset을 넘겨주어 웹에 출력
## database model  
1. 방송/연예 model  
기사ID : id = models.IntegerField(primary_key=True)  
기사항목 : category = models.CharField(max_length=10) 
기사제목 : title = models.TextField(max_length=100)  
기사내용 : content = models.TextField()  
기사업로드날짜 : uploadDate = models.CharField(max_length=10)  
DB업데이트날짜 : updateDate = models.DateTimeField()  
2. to do  
나머지 기사 모델, 역인덱스 모델  
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
**18.5.13**  
1.지금까지는 방송/연예 기사 전체 약 7만 개의 기사 중, 테스트를 위해 50개의 기사만 크롤링 했었다.  
오늘은 7만 개의 기사를 수집하기 위해 크롤러를 돌려봤는데 800번도 못 가서 에러가 났다.  
에러가 난 부분의 기사를 웹에서 접속해봤더니 삭제된 기사였다.  
그래서 웹문서를 가져올 때 삭제된 부분은 넘어가도록 조건을 주었더니 잘된다.  
2.본격적으로 기사 수집에 들어갔다. 근데 1만개의 기사를 수집하는데만 40분이 넘게 걸린 것 같다.(중간에 종료해버려서 정확하진 않지만 체감상..) 그래서 병렬 처리의 필요성을 느꼈다. 구글링을 해보니 "프로세스는 CPU코어(Hyper-Thread인 경우 2배) 개수의 2배(ex: 4코어 i5는 8개, 4코어8스레드인 i7은 16개)로 하면 가장 빠르지는 않지만 적당히 빠른 속도를 가져다줍니다."라고 한다. 내 노트북은 i5여서 8개의 프로세스를 만들었다. 그러나 전체 기사를 8등분 하려니 여러 조건들이 필요했다. n개의 기사를 8등분하려면 n/8의 간격으로 기사번호를 나누고, 페이지 번호는 한 페이지당 기사가 20개 이므로 20개당 1개씩 늘려줘야 하고 해당 페이지에서 몇 번째 기사인지도 count해줘야한다. n등분이 돼서 이런 것들에 대한 인덱스가 너무 헷갈렸다.  
머릿속으로만 하다가 실패해서 노트에다가 for문에 대한 인덱스를 적고 디버깅을 해가며 비교하니 답이 나왔다. 결국 완성했다ㅠ  
3. 현재 쓰고 있는 bs4모듈의 parser인 html.parser보다 lxml이 더 빠르다고 한다. paser를 바꿔 실행해보니 out of index라는 오류가 뜬다. 왜 그러는지 한참 고민하다가 뽐뿌 사이트를 들어가보니 서버가 다운됐다?-.- 내일 다시 해보자  
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
