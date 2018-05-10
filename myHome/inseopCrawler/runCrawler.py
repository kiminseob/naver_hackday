from bs4 import BeautifulSoup as bs
import requests
import re
from myHome.inseopCrawler import newsCrawler

title_num= [0 for _ in range(6)] #기사 컨텐츠 갯수


def start():
	'''
    서버에서 gzip 압축을 해서 응답을 하기 때문에 이를 클라이언트에서 풀지 못한다.
    헤더에 Accept-Encoding을 지정하여, 요청 시에 해당 헤더를 제외시켜서 gzip 압축을 하지 않도록 한다.
    Accept-Encoding은 requests.get함수에서 자동으로 세팅하는 함수
	'''
	headers = {'Accept-Encoding': None}
	URL = "http://www.ppomppu.co.kr/recent_main_article.php?type=news" #뽐뿌 뉴스 url
	ppomppu_developerForum_html=requests.get(URL, headers=headers)
	soup = bs(ppomppu_developerForum_html.text, "html.parser")
	p = re.compile("&no=")  # 기사 별로 컨텐츠 갯수를 추려냄
	for i in range(6):
		if i<3:
			title_ul=soup.findAll('ul',{'class':'ppomppu_board01'})[i] #뉴스 테이블 1열
		else:
			title_ul = soup.findAll('ul', {'class': 'ppomppu_board02'})[i-3] #뉴스 테이블 2열
		title_link = title_ul.findAll('a')[1].get('href') #게시물 최신 링크주소를 가져온다.
		title_num[i] = p.split(title_link)[1] # 각 뉴스 별 게시물 총 갯수 추출

	newsCrawler.broadcast(headers,title_num[0]) #방송/연예기사 크롤링
