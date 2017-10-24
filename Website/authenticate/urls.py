from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^/connexion$', views.connexion, name='connexion'),
    url(r'^/inscription$', views.inscription, name='inscription'),
    url(r'^/deconnexion$', views.deconnexion, name='deconnexion'),
    url(r'^/user$', views.userview, name='user'),
    url(r'^/user/mycolumns/(\d+)$', views.userarticles, name='mycolumns'),
    url(r'^/user/savedcolumns/(\d+)$', views.savedarticles, name='savedcolumns'),
    url(r'^/user/profil$', views.profil, name='profil'),
]
