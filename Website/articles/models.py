# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    titre = models.CharField(max_length=100)
    sous_titre = models.CharField(max_length=400)
    photo = models.ImageField(upload_to='photos_articles', default = 'photos_articles/default.jpg')
    auteur = models.ForeignKey(User)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, 
                                verbose_name="Date de parution")
    categorie = models.ForeignKey('Categorie')
    likes = models.IntegerField(default=0)
    ranking = models.FloatField(default=0)
    url = models.CharField(max_length=500, default = '/')
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.titre

class Categorie(models.Model):
    nom = models.CharField(max_length=30)
    colour = models.CharField(max_length=30)
    def __str__(self):
        return self.nom

class Comment(models.Model):
    auteur = models.ForeignKey(User)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de parution")
    article = models.ForeignKey('Article')
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.auteur

class Channel(models.Model):
    titre = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    photo = models.ImageField(upload_to='photos_articles', default = 'photos_articles/default.jpg')
    administrateur = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, 
                                verbose_name="Date de creation")
    ranking = models.FloatField(default=0)
    url = models.CharField(max_length=500, default = '/')
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.titre

class Channel_Ask(models.Model):
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de demande")
    channel = models.ForeignKey('Channel')
    article = models.ForeignKey('Article')
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.article

class Channel_Belong(models.Model):
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de demande")
    channel = models.ForeignKey('Channel')
    article = models.ForeignKey('Article')
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.article

class Like(models.Model):
    auteur = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de parution")
    article = models.ForeignKey('Article')
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.auteur

class Save(models.Model):
    auteur = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de parution")
    article = models.ForeignKey('Article')
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.auteur

class Signature(models.Model):
    user = models.ForeignKey(User)
    signature = models.CharField(max_length=50)
    bio = models.CharField(max_length=400)
    def __str__(self):
        return self.user