from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from myHome.models import NEWS_BROADCAST
from urllib import parse
import os

#   방송/연예 기사 크롤링   # 
def broadcast(title_num,end_num, page_num,count,q): #기사 제목,내용,날짜 크롤링
	url_params = {  # 뉴스 URL에 넘겨줄 파라미터
		"id": "news_broadcast",
		"page": "",
		"divpage": "16",
		"no": ""
	}
	uploaded = [0 for _ in range(20)] #업로드날짜 저장 (한 페이지=기사20개씩)
	URL = "http://www.ppomppu.co.kr/zboard/view.php" #기사 주소
	
	uploaded = uploadDate(url_params,page_num)  #해당 페이지에 있는 20개의 기사 업로드 날짜 크롤링
	
	for i in range(int(title_num),end_num,-1): #전체 기사 갯수만큼 for문을 반복
		count+=1
		if count%21==0: #한 페이지에 기사가 20개씩 있으므로 20개마다 한 페이지 넘어감.
			count=1
			page_num+=1
			uploaded =uploadDate(url_params,page_num)  #페이지 넘어갈 때마다 20개의 기사 업로드 날짜 크롤링
		try:
			row = NEWS_BROADCAST.objects.get(pk=i)
			print("%d번 : 지나친다~~~"%(i))
			continue
		except Exception as e:
			print("들어옴")
			q.put("{0}번 프로세스 : {1}번 기사 수집".format(os.getpid(),i))
			url_params.__setitem__("page",page_num) #기사 페이지
			url_params.__setitem__("no", i)         #기사 번호
			news_broadcast_html = requests.get(URL, headers = {'Accept-Encoding': None}, params=url_params) #방송/연예 기사 웹문서 가져온다.
			soup = bs(news_broadcast_html.content, "lxml")
			view_title = soup.find("td", {"class": "view_title"})
			view_content = soup.findAll("table", {"class": "pic_bg"})
			title=""
			content=""
			if view_title != None:
				title = soup.find("td", {"class": "view_title"}).text.strip()  # 방송/연예 기사의 제목
				if view_content:
					content = view_content[3].find("table").text.strip() # 방송/연예 기사의 내용
			#DB에 저장
			wdTable = NEWS_BROADCAST(id=i, category="방송/연예", title=title, content=content,uploadDate=uploaded[count-1].text,updateDate=datetime.now())
			wdTable.save()

#   방송/연예 기사 올라온 날짜 크롤링   #
def uploadDate(url_params, page_num):
	URL = "http://www.ppomppu.co.kr/zboard/zboard.php" #방송/연예 기사 테이블
	url_params.__setitem__("page",page_num)
	new_table = requests.get(URL, headers = {'Accept-Encoding': None}, params=url_params)
	soup = bs(new_table.text,"html.parser")
	dates = soup.findAll('span',{'class':'gallery_data'})
	return dates
	
	
