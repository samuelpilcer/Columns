from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.homepage),
    url(r'^accueil$', views.home, name="accueil"),
    url(r'^accueil/(\d+)$', views.read_page, name='list_articles'),
    url(r'^article/tag/(?P<id>\d{4})/(?P<page>\d{2})$', views.read_by_tag, name='tag_articles'),
    url(r'^article/search/(?P<phrase>[\w\-]+)/(?P<nb>\d+)$', views.search_page, name='search'),
    url(r'^article/search/(?P<phrase>[\w\-]+)$', views.search, name='search_p0'),
    url(r'^article/search_by_form$', views.search_form, name='search_by_form'),
    url(r'^article/tag/(\d+)$', views.read_by_tag_p0, name='tag_articles_p0'),
    url(r'^article/(\d+)$', views.lire, name='lire'),
    url(r'^article/like/(\d+)$', views.like, name='like'),
    url(r'^article/save/(\d+)$', views.save, name='save'),
    url(r'^article/new$', views.new, name='new'),
    url(r'^article/actualize_rank$', views.actualize_rank, name='actualize_rank'),
    url(r'^user/(?P<user>[\w\-]+)/(?P<article_url>[\w\-]+)$', views.get_article, name='get_article'),
    url(r'^analytics/(\d+)$', views.metrics, name='analytics'),
    url(r'^twitter/$', views.tweets, name='tweets'),
    url(r'^twitter/analyze/(?P<hashtag>[\w\s]+)$', views.tweets_analyze, name='tweets_analyze'),
    url(r'^new_channel$', views.new_channel, name='new_channel'),
    url(r'^channels$', views.list_channels, name='list_channels'),
    url(r'^channels/(?P<channel_url>[\w\-]+)$', views.channel_articles, name='channel_articles'),
    url(r'^users/(?P<page>\d+)$', views.list_users, name='list_users'),
    url(r'^users$', views.list_users_p0, name='list_users_p0'),
    url(r'^add_to_channel/(\d+)$', views.add_to_channel, name='add_to_channel'),
    url(r'^remove_from_channel/(?P<id_article>\d+)/(?P<id_fil>\d+)$', views.delete_from_fil, name='delete'),
]
