
from django.contrib import admin
from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
urlpatterns = [
    
    url(r'^admin/',admin.site.urls),
    url(r'^',include('GRsystem.urls'))
    
]
admin.site.site_header = "NCI Admin"
admin.site.site_title = "NCI Admin Portal"
admin.site.index_title = "Welcome to NCI Admin Portal"