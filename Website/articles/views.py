# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

from articles.models import Article, Categorie, Comment, Like, Save, Signature

def homepage(request):
    return redirect('/accueil')

def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    articles = Article.objects.all() # Nous sélectionnons tous nos articles

    if len(articles)>10:
        n=5
    else:
        n=int(len(articles)/2)

    articles1=[]
    articles2=[]
    for i in range(n):
        articles1.append(articles[2*i])
        articles2.append(articles[2*i+1])

    if len(articles)<10 and 2*int(len(articles)/2) != len(articles):
        articles1.append(articles[len(articles)-1])
    
    bool_prec=False
    bool_suiv=True

    return render(request, 'blog/accueil.html', {'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':1, 'page_prec':0,'bool_suiv': bool_suiv, 'bool_prec': bool_prec})

def read_page(request, nb):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    articles = Article.objects.all() # Nous sélectionnons tous nos articles
    nb=int(nb)
    if len(articles)>10+10*nb:
        n=5
        bool_suiv=True
    elif (len(articles)<=10+10*nb) and (len(articles)>=10*nb):
        n=int((len(articles)-10*nb)/2)
        bool_suiv=False
    else:
        return redirect('/accueil')

    articles1=[]
    articles2=[]
    for i in range(n):
        articles1.append(articles[2*i+10*nb])
        articles2.append(articles[2*i+1+10*nb])

    if len(articles)<=10+10*nb and 2*int((len(articles)-10*nb)/2)+10*nb != len(articles):
        articles1.append(articles[len(articles)-1])

    if nb>0:
        page_prec=nb-1
        bool_prec=True
    else:
        page_prec=0
        bool_prec=False
    page_suiv=nb+1

    return render(request, 'blog/accueil.html', {'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':page_suiv, 'page_prec':page_prec, 'bool_suiv': bool_suiv, 'bool_prec': bool_prec})


def read_by_tag(request, id, nb):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    try:
        categorie = Categorie.objects.get(id=id)
        articles = Article.objects.all().filter(categorie=categorie) # Nous sélectionnons tous nos articles
    except:
        articles=[]

    nb=int(nb)
    if len(articles)>10+10*nb:
        n=5
        bool_suiv=True
    elif (len(articles)<=10+10*nb) and (len(articles)>=10*nb):
        n=int((len(articles)-10*nb)/2)
        bool_suiv=False
    else:
        return redirect('/accueil')

    articles1=[]
    articles2=[]
    for i in range(n):
        articles1.append(articles[2*i+10*nb])
        articles2.append(articles[2*i+1+10*nb])

    if len(articles)<=10+10*nb and 2*int((len(articles)-10*nb)/2)+10*nb != len(articles):
        articles1.append(articles[len(articles)-1])

    if nb>0:
        page_prec=nb-1
        bool_prec=True
    else:
        page_prec=0
        bool_prec=False
    page_suiv=nb+1

    return render(request, 'blog/accueil.html', {'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':page_suiv, 'page_prec':page_prec, 'bool_suiv': bool_suiv, 'bool_prec': bool_prec})


def read_by_tag_p0(request, id):
    return read_by_tag(request, id, 0)


def lire(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404
    try:
        likes = Like.objects.all().filter(article=article)
        number_of_likes=len(likes)
    except:
        number_of_likes=0
    try:
        like_from_user = Like.objects.all().filter(article=article).filter(auteur=request.user)
        if len(like_from_user)>0:
            has_liked=True
        else:
            has_liked=False
    except:
        has_liked=False

    form = CommentForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        new_comment=Comment()
        new_comment.auteur=request.user
        new_comment.contenu = form.cleaned_data.get('contenu')
        new_comment.article = article
        new_comment.save()

        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True

    try:
        comments=Comment.objects.all().filter(article=article)
    except:
        comments=[]

    try:
        signature = Signature.objects.get(user=article.auteur).signature
    except:
        signature = article.auteur.first_name+" "+article.auteur.last_name

    return render(request, 'blog/lire.html', {'article': article, 'form':form, 'comments': comments, 'has_liked':has_liked, 'number_of_likes':number_of_likes, 'signature':signature})

@login_required
def new(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = ArticleForm(request.POST or None)
    # Nous vérifions que les données envoyées sont valides
    # Cette méthode renvoie False s'il n'y a pas de données 
    # dans le formulaire ou qu'il contient des erreurs.
    if form.is_valid(): 
        # Ici nous pouvons traiter les données du formulaire
        new_article=Article()
        new_article.auteur=request.user
        new_article.titre = form.cleaned_data.get('titre')
        new_article.contenu = form.cleaned_data.get('contenu')
        new_article.categorie = form.cleaned_data.get('categorie')
        new_article.save()

        # Nous pourrions ici envoyer l'e-mail grâce aux données 
        # que nous venons de récupérer
        envoi = True
    
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'blog/new.html', locals())

@login_required
def like(request, id):
    article=Article.objects.get(id=id)
    try:
        like_from_user = Like.objects.all().filter(article=article).filter(auteur=request.user)
        if len(like_from_user)>0:
            user_liked=True
        else:
            user_liked=False
    except:
        user_liked=False

    if user_liked:
        like_from_user[0].delete()
    else:
        new_like=Like()
        new_like.auteur=request.user
        new_like.article = article
        new_like.save()
    return redirect('/article/'+id)

@login_required
def save(request, id):
    article=Article.objects.get(id=id)
    try:
        like_from_user = Save.objects.all().filter(article=article).filter(auteur=request.user)
        if len(like_from_user)>0:
            user_liked=True
        else:
            user_liked=False
    except:
        user_liked=False

    if user_liked:
        like_from_user[0].delete()
    else:
        new_like=Save()
        new_like.auteur=request.user
        new_like.article = article
        new_like.save()
    return redirect('/article/'+id)