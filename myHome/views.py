from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from myHome.models import NEWS_BROADCAST
from myHome.inseopCrawler import newsCrawler
from myHome.inseopCrawler import runCrawler

# Create your views here.
@csrf_exempt 
def index(request):
	broadcasts = NEWS_BROADCAST.objects.all() #해당 디비의 모든 정보를 가져온다.
	broadcasts = broadcasts.order_by('-id')  #기사 최신순 정렬.
	context = {'broadcasts':broadcasts}
	return render(request,'myHome/index.html',context)
@csrf_exempt 
def contents(request):
	return render(request,'myHome/contents.html',{})

def startCrawler(request):
	return render(request,'myHome/startCrawler.html',{})		
		
def stopCrawler(request):
	return render(request,'myHome/stopCrawler.html',{})	
		
