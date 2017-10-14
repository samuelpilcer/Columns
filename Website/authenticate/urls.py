from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^/connexion$', views.connexion, name='connexion'),
    url(r'^/inscription$', views.inscription, name='inscription'),
    url(r'^/deconnexion$', views.deconnexion, name='deconnexion'),
]
