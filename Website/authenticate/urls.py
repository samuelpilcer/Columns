from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^/connexion$', views.connexion, name='connexion'),
    url(r'^/inscription$', views.inscription, name='inscription'),
    url(r'^/deconnexion$', views.deconnexion, name='deconnexion'),
    url(r'^/user$', views.userview, name='user'),
    url(r'^/user/mycolumns/(\d+)$', views.userarticles, name='mycolumns'),
    url(r'^/user/mycolumns/', views.userarticles_p0, name='mycolumns_p0'),
    url(r'^/user/savedcolumns/(\d+)$', views.savedarticles, name='savedcolumns'),
    url(r'^/user/profil$', views.profil, name='profil'),
    url(r'^/user/pwd$', views.change_password, name='change_password'),
    url(r'^article/delete/(\d+)$', views.delete, name='delete'),
    url(r'^/user/(?P<userurl>[\w\-]+)/$', views.hiscolumns_p0, name='hiscolumns_po'),
    url(r'^/user/(?P<userurl>[\w\-]+)/(\d+)$', views.hiscolumns, name='hiscolumns'),
]