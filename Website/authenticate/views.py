# coding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import ConnexionForm, InscriptionForm, SignatureForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from articles.models import Article, Save, Signature
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'connexion.html', locals())

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))


def userview(request):
    return render(request, 'user.html')

@login_required
def userarticles(request, nb):

    try:
        articles = Article.objects.all().filter(auteur=request.user) # Nous sélectionnons tous nos articles
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

    return render(request, 'mycolumns.html', {'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':page_suiv, 'page_prec':page_prec, 'bool_suiv': bool_suiv, 'bool_prec': bool_prec})

@login_required
def profil(request):
    if request.method == "POST":
        signature_form = SignatureForm(request.POST)
        if signature_form.is_valid():
            try:
                obj = Signature.objects.get(user=request.user)
                obj.signature = signature_form.cleaned_data.get('signature')
                obj.bio=signature_form.cleaned_data.get('bio')
                obj.save()
            except Signature.DoesNotExist:
                obj=Signature()
                obj.user=request.user
                obj.bio=signature_form.cleaned_data.get('bio')
                obj.signature = signature_form.cleaned_data.get('signature')
                obj.save()
    else:
        try:
            obj = Signature.objects.get(user=request.user)
            signature_form = SignatureForm(instance=obj)
        except Signature.DoesNotExist:
            signature_form = SignatureForm()
    return render(request, 'profil.html', {'form': signature_form})

@login_required
def delete(request, id):
    try:
        article=Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404

    if article.auteur==request.user:
        article.delete()

    return redirect("accueil")

@login_required
def savedarticles(request, nb):

    try:
        saved = Save.objects.all().filter(auteur=request.user) # Nous sélectionnons tous nos articles
    except:
        saved = []

    articles=[]
    for i in saved:
        articles.append(i.article)

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

    return render(request, 'savedcolumns.html', {'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':page_suiv, 'page_prec':page_prec, 'bool_suiv': bool_suiv, 'bool_prec': bool_prec})