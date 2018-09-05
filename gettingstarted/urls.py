from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^getall', hello.views.get_all, name='getall'),
    url(r'^get', hello.views.get_one, name='get'),
    url(r'^add', hello.views.add, name='add'),
    url(r'^remove', hello.views.remove_stock, name='remove'),
    url(r'^refresh', hello.views.refresh, name='refresh'),
    url(r'^unsubscribe', hello.views.unsubscribe, name='unsubscribe'),
    path('admin/', admin.site.urls),
]
