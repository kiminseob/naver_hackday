from urllib import parse
from django import template
from django.db.models import Q
from myHome.models import NEWS_BROADCAST
from myHome.sorting import Sort
import re
import pycurl
from io import BytesIO

register = template.Library()



'''
검색어가 포함된 URL과 queryset이 넘어오면
URL에서 검색어를 추출 후, 공백을 기준으로 키워드를 구분한다.
키워드가 기사의 제목 또는 내용과 일치하는 query가 있으면 해당 query를 합친 queryset과 queryset 갯수를 넘겨준다. 
'''
@register.simple_tag
def queryset_search(URL, model):
	URL = parse.unquote(URL)
	URL = URL.split("searchInput=")[1]
	searchInput = URL.split("&year=")[0]
	year = URL.split("year=")[1]
	year = year.split("&sort=")[0]
	sort = URL.split("&sort=")[1]
	searchInput = re.sub("[+]"," ",searchInput)
	split = " ".join(searchInput.split())
	keywords=split.split(" ")
	q_objects = Q()

	#전체 검색
	if year=="all":
		for keyword in keywords:
			q_objects.add(Q(content__contains=keyword), Q.OR)
			q_objects.add(Q(title__contains=keyword), Q.OR)
		
	#년도별 검색
	else:
		year = year.split("20")[1]
		print(year)
		for keyword in keywords:
			q_objects.add(Q(content__contains=keyword), Q.OR)
			q_objects.add(Q(title__contains=keyword), Q.OR)
			q_objects.add(Q(uploadDate__startswith=year), Q.AND)

	queryset = NEWS_BROADCAST.objects.filter(q_objects)
	
	#일치하는 쿼리문이 존재하지 않으면
	if not queryset:
		return False
	
	#최신순 정렬
	if sort=="recent":
		queryset = queryset.order_by('-id')
	#정확도 순 : 일치하는 키워드의 갯수가 많은 순서(제목,내용)
	elif sort=="accuracy":
		global queryset
		i=0
		id = [0 for _ in range(queryset.count())]
		count =  [0 for _ in range(queryset.count())]
		match_cnt = {"id":id,"count":count}
		for q in queryset:
			title = q.title
			content = q.content
			count=0
			for keyword in keywords:
				a = re.findall(keyword,title)
				b = re.findall(keyword, content)
				count +=a.__len__() + b.__len__()
			id = match_cnt.get('id')
			cnt = match_cnt.get('count')
			id[i] = q.id
			cnt[i] = count
			match_cnt.__setitem__("id",id)
			match_cnt.__setitem__("count",cnt)
			i+=1
		Sort.quickSort(match_cnt.get("count"),match_cnt.get("id"),0,match_cnt.get("id").__len__()-1)
		temp = Q() 
		for i in range(match_cnt.get("id").__len__()-1,0,-1):
			a = int(match_cnt.get("id")[i])
			temp.add(Q(pk=a),Q.OR)
		
		queryset = NEWS_BROADCAST.objects.filter(temp)
		print(queryset)		
					
	context = {'broadcasts':queryset,'queryset_length':queryset.count(), 'keywords':keywords}
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
	
'''
키워드를 반환
'''
@register.simple_tag
def keywords(URL):
	URL = parse.unquote(URL)
	try:
		URL = URL.split("keywords=")[1]
		searchInput = re.sub("[\+\'\,\[\]]", " ", URL)
		split = " ".join(searchInput.split())
		keywords = split.split(" ")
		print(keywords)
		context = {"keywords":keywords}
		return context
	except IndexError as e:
		print(e)
		return {}
'''
년도를 반환
'''
@register.simple_tag
def year(URL):
	try:
		URL = parse.unquote(URL)
		year = URL.split("year=")[1]
		year = year.split("&sort=")[0]
		if year =="all":
			return year
		year = int(year)
		return year
	except IndexError as e:
		print("년도반환{0}".format(e))
		return False

'''
기사 정렬
'''

@register.simple_tag
def sort(URL):
	try:
		URL = parse.unquote(URL)
		print(URL)
		sort = URL.split("sort=")[1]
		if sort=="recent":
			return False
		elif sort=="accuracy":
			return True
		return sort
	except IndexError as e:
		print("정렬반환{0}".format(e))
		return False




headers = {}
def header_function(header_line):
    # HTTP standard specifies that headers are encoded in iso-8859-1.
    # On Python 2, decoding step can be skipped.
    # On Python 3, decoding step is required.
    header_line = header_line.decode('iso-8859-1')

    # Header lines include the first status line (HTTP/1.x ...).
    # We are going to ignore all lines that don't have a colon in them.
    # This will botch headers that are split on multiple lines...
    if ':' not in header_line:
        return

    # Break the header line into header name and value.
    name, value = header_line.split(':', 1)

    # Remove whitespace that may be present.
    # Header lines include the trailing newline, and there may be whitespace
    # around the colon.
    name = name.strip()
    value = value.strip()

    # Header names are case insensitive.
    # Lowercase name here.
    name = name.lower()

    # Now we can actually record the header name and value.
    # Note: this only works when headers are not duplicated, see below.
    headers[name] = value


@register.simple_tag
def apache():

	buffer = BytesIO()
	c = pycurl.Curl()
	c.setopt(c.URL, 'localhost:2000/mod_inseop')
	c.setopt(c.WRITEFUNCTION, buffer.write)
# Set our header function.
	c.setopt(c.HEADERFUNCTION, header_function)
	c.perform()
	c.close()

# Figure out what encoding was sent with the response, if any.
# Check against lowercased header name.
	encoding = None
	if 'content-type' in headers:
    		content_type = headers['content-type'].lower()
    		match = re.search('charset=(\S+)', content_type)
    		if match:
        		encoding = match.group(1)
        		print('Decoding using %s' % encoding)
	if encoding is None:
    # Default encoding for HTML is iso-8859-1.
    # Other content types may have different default encoding,
    # or in case of binary data, may have no encoding at all.
    		encoding = 'iso-8859-1'
    		print('Assuming encoding is %s' % encoding)

	body = buffer.getvalue()
# Decode using the encoding we figured out.
	print(body.decode(encoding))	
