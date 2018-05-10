from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from myHome.models import NEWS_BROADCAST

#   방송/연예 기사 크롤링   # 
def broadcast(headers,title_num): #기사 제목,내용,날짜 크롤링
	url_params = {  # 뉴스 URL에 넘겨줄 파라미터
		"id": "news_broadcast",
		"page": "",
		"divpage": "16",
		"no": ""
	}
	uploaded = [0 for _ in range(20)] #업로드날짜 저장 (한 페이지=기사20개씩)
	count=0    #한 페이지 당 기사 갯수 카운트
	page_num=1 #페이지 수
	URL = "http://www.ppomppu.co.kr/zboard/view.php" #기사 주소
	for i in range(int(title_num),int(title_num)-50,-1): #전체 기사 갯수만큼 for문을 반복
		count+=1
		uploaded = uploadDate(headers,url_params,page_num,count)  #첫 페이지에 있는 20개의 기사 업로드 날짜 크롤링
		if count%20==0: #한 페이지에 기사가 20개씩 있으므로 20개마다 한 페이지 넘어감.
			count=1
			page_num+=1
			uploaded =uploadDate(headers,url_params,page_num,count)  #페이지 넘어갈 때마다 20개의 기사 업로드 날짜 크롤링
		url_params.__setitem__("page",page_num) #기사 페이지
		url_params.__setitem__("no", i)         #기사 번호
		news_broadcast_html = requests.get(URL, headers=headers, params=url_params) #방송/연예 기사 웹문서 가져온다.
		soup = bs(news_broadcast_html.text, "html.parser")
		title = soup.find("td",{"class":"view_title"}).text.strip()        #방송/연예 기사의 제목
		content = soup.findAll("table",{"class":"pic_bg"})[3].text.strip() #방송/연예 기사의 내용

		#DB에 저장
		wdTable = NEWS_BROADCAST(id=i, category="방송/연예", title=title, content=content,uploadDate=uploaded[count-1].text,updateDate=datetime.now())
		wdTable.save()

#   방송/연예 기사 올라온 날짜 크롤링   #
def uploadDate(headers, url_params, page_num, count):
	URL = "http://www.ppomppu.co.kr/zboard/zboard.php" #방송/연예 기사 테이블
	url_params.__setitem__("page",page_num)
	new_table = requests.get(URL, headers=headers, params=url_params)
	soup = bs(new_table.text,"html.parser")
	dates = soup.findAll('span',{'class':'gallery_data'})
	return dates
	
	