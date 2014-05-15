from django.conf.urls import patterns, include, url
from EventSource import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    #url(r'^$', 'EventSource.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', 'Main.views.home', name = 'home'),
    
    url(r'^Login/Fb/$', 'Main.views.fbLogin', name = 'fblogin'),
    
    url(r'^Logout/$', 'Main.views._logout', name = 'logout'),
    
    url(r'^Event/Submit/$', 'Main.views.newEvent', name = 'newevent'),

    url(r'^admin/', include(admin.site.urls))]  
    
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
