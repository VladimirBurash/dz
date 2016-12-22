"""lab7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconfF
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from my_app.views import login, signup,logout_view,shows_view,show_view,ajax_list
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/', signup, name='signup'),
    url(r'^logout/', logout, {'next_page': '/login/'}, name='logout'),
    url(r'^login/', login, name='login'),
    url(r'^index/$', logout_view, name='index'),
    url(r'^shows/$', shows_view, name='shows'),
    url(r'^ajax_list/(?P<page_id>[0-9]+)$', ajax_list, name='ajax_list'),
    url(r'^shows/(?P<show_id>\d+)$', show_view, name='show'),

]