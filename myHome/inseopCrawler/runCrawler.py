from bs4 import BeautifulSoup as bs
import requests
import re
from myHome.inseopCrawler import newsCrawler
from multiprocessing import Process, Queue

q = Queue()
process_list=[]

def start():
	global q,process_list
	q.put(1)
	title_num= [0 for _ in range(6)] #기사 컨텐츠 갯수
	'''
    서버에서 gzip 압축을 해서 응답을 하기 때문에 이를 클라이언트에서 풀지 못한다.
    헤더에 Accept-Encoding을 지정하여, 요청 시에 해당 헤더를 제외시켜서 gzip 압축을 하지 않도록 한다.
    Accept-Encoding은 requests.get함수에서 자동으로 세팅하는 함수
	'''
	URL = "http://www.ppomppu.co.kr/recent_main_article.php" #뽐뿌 뉴스 url
	ppomppu_developerForum_html=requests.get(URL, headers = {'Accept-Encoding': None},params= { "type": "news"})
	soup = bs(ppomppu_developerForum_html.content, "lxml")
	p = re.compile("&no=")  # 기사 별로 컨텐츠 갯수를 추려냄
	try:
		for i in range(6):
			if i<3:
				title_ul=soup.findAll('ul',{'class':'ppomppu_board01'})[i] #뉴스 테이블 1열
			else:
				title_ul = soup.findAll('ul', {'class': 'ppomppu_board02'})[i-3] #뉴스 테이블 2열
			title_link = title_ul.findAll('a')[1].get('href') #게시물 최신 링크주소를 가져온다.
			title_num[i] = p.split(title_link)[1] # 각 뉴스 별 게시물 총 갯수 추출

		divided_index=round(int(title_num[0])/8)
		page=(divided_index/20)+1   #기사가 있는 페이지 번호
		count=divided_index%20  #해당 페이지의 count 번째 기사
		divide = int(title_num[0])-divided_index
		next_page=page
		next_count=count
		for i in range(8):
			if i==0:
				#print("i=0 : title_num:%s , divide:%d, page:1, count:0"%(title_num[0],divide))
				proc = Process(target=newsCrawler.broadcast, args=(title_num[0],divide,1,0,q))#기사 크롤링
				
			else:
				if i==7:
					#print("i=7 : title_num:%d, divide:0, page:%d, count:%d"%(divide,next_page,next_count))
					proc = Process(target=newsCrawler.broadcast, args=(divide,0,next_page,next_count,q))#기사 크롤링
				else:
					title_num[0]=divide
					divide = int(title_num[0])-divided_index
					#print("else : title_num:%d , divide:%d, page:%d, count:%d"%(title_num[0],divide,next_page,next_count))
					proc = Process(target=newsCrawler.broadcast, args=(title_num[0],divide,next_page,next_count,q))#기사 크롤링
				next_page=next_page+page-1
				next_count=(next_count+count)%20
			
			proc.daemon = False
			process_list.append(proc)
			proc.start()
		return True
	except IndexError as e:
		print(e)
		return False

def emptyQ():
	global q
	return q.empty()

def terminate_process():
	global process_list
	for i in range(len(process_list)):
		process_list[i].terminate()

def clearQ():
	global q,process_list
	q =Queue()
	process_list=[]

def sizeQ():
	global q
	return q.qsize()

	
	