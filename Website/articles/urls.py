from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.homepage),
    url(r'^accueil$', views.home),
    url(r'^accueil/(\d+)$', views.read_page, name='list_articles'),
    url(r'^article/tag/(?P<id>\d{4})/(?P<page>\d{2})$', views.read_by_tag, name='tag_articles'),
    url(r'^article/tag/(\d+)$', views.read_by_tag_p0, name='tag_articles_p0'),
    url(r'^article/(\d+)$', views.lire, name='lire'),
    url(r'^article/like/(\d+)$', views.like, name='like'),
    url(r'^article/new$', views.new, name='new'),
]
