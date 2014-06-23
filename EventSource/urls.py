from django.conf.urls import patterns, include, url
from EventSource import settings
from django.conf.urls.static import static
from Login.views import Login

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    
    url(r'^$', Login.as_view(), name = 'home'),
    
    url(r'^Home/$', 'Main.views.home', name = 'main'),
    
    url(r'^Login/Fb/$', 'Login.views.fbLogin', name = 'fblogin'),
    
    url(r'^Login/$', Login.as_view(), name = 'login'),
    
    url(r'^Logout/$', 'Login.views._logout', name = 'logout'),
    
    url(r'^Event/Submit/$', 'Main.views.newEvent', name = 'newevent'),
    
    url(r'^NewEvent/EventPhoto/Upload/', 'Main.views.newEventFileUpload', name = 'newEvent_fileUpload'),

    url(r'^admin/', include(admin.site.urls))]  
    
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
