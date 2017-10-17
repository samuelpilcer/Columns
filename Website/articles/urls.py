from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.homepage),
    url(r'^accueil$', views.home),
    url(r'^accueil/(\d+)$', views.read_page, name='list_articles'),
    url(r'^article/(\d+)$', views.lire, name='lire'),
    url(r'^article/new$', views.new, name='new'),
]
