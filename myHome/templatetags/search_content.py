from urllib import parse
from django import template
from django.db.models import Q
from myHome.models import NEWS_BROADCAST
from django.contrib.postgres.search import SearchVector
#from konlpy.tag import Twitter
import re
register = template.Library()

'''
검색어가 포함된 URL과 queryset이 넘어오면
URL에서 검색어를 추출 후, 공백을 기준으로 키워드를 구분한다.
키워드가 기사의 제목 또는 내용과 일치하는 query가 있으면 해당 query를 합친 queryset과 queryset 갯수를 넘겨준다. 
'''
@register.simple_tag
def queryset_search(URL, model):
	#twitter = Twitter()
	URL = parse.unquote(URL)  
	searchInput = URL.split("searchInput=")[1]
	searchInput = re.sub("[+]"," ",searchInput)
	#keywords=searchInput.split(" ")
	#keywords=twitter.nouns(searchInput)
	split = " ".join(searchInput.split())
	keywords=split.split(" ")
	print(keywords)
	q_objects = Q()
	for keyword in keywords:
		q_objects.add(Q(content__contains=keyword), Q.OR)
		q_objects.add(Q(title__contains=keyword), Q.OR)

	queryset = NEWS_BROADCAST.objects.filter(q_objects)
	queryset_len = queryset.count()

	if not queryset:
		return False
	queryset = queryset.order_by('-id')  #기사 최신순 정렬.
	context = {'broadcasts':queryset,'queryset_length':queryset.count()}
	return context

'''
검색된 값이 있는지 체크한다.
검색된 값이 없다면 False를 반환.
검색된 값이 있으면 True를 반환.
'''
@register.filter
def search_input_check(URL):
	try:
		URL = parse.unquote(URL)  
		searchInput = URL.split("searchInput=")[1]
		m = re.search('[^+\t\n\r\f\v]',searchInput)
		if m:
			return True
		else:
			return False
	except IndexError:
		return False
	

