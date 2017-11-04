from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.homepage),
    url(r'^accueil$', views.home, name="accueil"),
    url(r'^accueil/(\d+)$', views.read_page, name='list_articles'),
    url(r'^article/tag/(?P<id>\d{4})/(?P<page>\d{2})$', views.read_by_tag, name='tag_articles'),
    url(r'^article/search/(?P<id>\d{4})/(?P<page>\d{2})$', views.search_page, name='search'),
    url(r'^article/search/(?P<id>\d{4})$', views.search, name='search_p0'),
    url(r'^article/search_by_form$', views.search_form, name='search_by_form'),
    url(r'^article/tag/(\d+)$', views.read_by_tag_p0, name='tag_articles_p0'),
    url(r'^article/(\d+)$', views.lire, name='lire'),
    url(r'^article/like/(\d+)$', views.like, name='like'),
    url(r'^article/save/(\d+)$', views.save, name='save'),
    url(r'^article/new$', views.new, name='new'),
    url(r'^article/actualize_rank$', views.actualize_rank, name='actualize_rank'),
    url(r'^(?P<user>\d+)/(?P<article>\d+)$', views.get_article, name='get_article'),
]
