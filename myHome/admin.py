from django.contrib import admin
from myHome.models import NEWS_BROADCAST
# Register your models here.
class viewAdmin(admin.ModelAdmin):
	list_display = ('id','category','title','content','uploadDate','updateDate')
admin.site.register(NEWS_BROADCAST, viewAdmin)
