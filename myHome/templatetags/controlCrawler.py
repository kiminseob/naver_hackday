from myHome.inseopCrawler import runCrawler
from django import template

register = template.Library()

# 크롤러를 동작시킨다. #
@register.simple_tag
def start():
	try:
		q=runCrawler.start()
		return True
	except IndexError as e:
		return False
		
# 크롤러 동작 상태 체크(큐를 체크) #
@register.simple_tag
def emptyQ_check():
	return runCrawler.emptyQ()

# 멀티 프로세스들 종료시키고 큐를 초기화한다. #
@register.simple_tag
def exitProcess():
	runCrawler.terminate_process()
	runCrawler.clearQ()
	return True
