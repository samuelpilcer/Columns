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
    time_to_read = models.IntegerField(default=0)
    url = models.CharField(max_length=500, default = '/')
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.titre


class UserData(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    ranking = models.FloatField(default=0)
    number_articles = models.IntegerField(default=0)
    number_logs = models.IntegerField(default=0)
    number_likes = models.IntegerField(default=0)
    number_saved = models.IntegerField(default=0)
    number_articles_he_liked = models.IntegerField(default=0)
    number_comments = models.IntegerField(default=0)
    number_articles_he_commented = models.IntegerField(default=0)


class Categorie(models.Model):
    nom = models.CharField(max_length=30)
    colour = models.CharField(max_length=30)
    def __str__(self):
        return self.nom

class Fil(models.Model):
    nom = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='photos_articles', default = 'photos_articles/default.jpg')
    description = models.TextField(null=True)
    admin = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de creation")
    ranking = models.FloatField(default=0)
    url = models.CharField(max_length=500, default = '/')
    def __str__(self):
        return self.nom

class InFil(models.Model):
    message = models.CharField(max_length=30,default = '')
    article = models.ForeignKey('Article')
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de parution")
    fil = models.ForeignKey('Fil')

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

class Like(models.Model):
    auteur = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de parution")
    article = models.ForeignKey('Article')
    def __str__(self):
        return unicode(self.auteur)

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