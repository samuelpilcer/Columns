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
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from articles.models import UserData
from chartit import DataPool, Chart
#from django.core.mail import EmailMessage
#from .tokens import account_activation_token

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
                try:
                    user_data=UserData.objects.all().filter(user=user)[0]
                    user_data.number_logs=user_data.number_logs+1
                    user_data.save()
                except:
                    UserData(user).save()
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
            #For next version with email verif: https://farhadurfahim.github.io/post/django-registration-with-confirmation-email/
            #user.is_active = False
            #form.save()
            #current_site = get_current_site(request)
            #message = render_to_string('acc_active_email.html', {
            #    'user':user, 
            #    'domain':current_site.domain,
            #    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #    'token': account_activation_token.make_token(user),
            #})
            #mail_subject = 'Activate your blog account.'
            #to_email = form.cleaned_data.get('email')
            #email = EmailMessage(mail_subject, message, to=[to_email])
            #email.send()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            UserData(user=user).save()
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
def userarticles_p0(request):
    return userarticles(request,0)

@login_required
def userarticles(request, nb):

    try:
        articles = Article.objects.all().filter(auteur=request.user).order_by('-date') # Nous sélectionnons tous nos articles
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

    return render(request, 'mycolumns.html', {'is_my_columns':True,'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':page_suiv, 'page_prec':page_prec, 'bool_suiv': bool_suiv, 'bool_prec': bool_prec})

@login_required
def promote_list_p0(request):
    return promote_list(request,0)

@login_required
def promote_list(request, nb):

    try:
        articles = Article.objects.all().filter(auteur=request.user).order_by('-date') # Nous sélectionnons tous nos articles
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

    return render(request, 'mycolumns.html', {'is_my_columns':False,'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':page_suiv, 'page_prec':page_prec, 'bool_suiv': bool_suiv, 'bool_prec': bool_prec})


def unroll_user_url(url):
    return url.split('-')[-1]

def hiscolumns_p0(request, userurl):
    return hiscolumns(request,userurl,0)

def hiscolumns(request, userurl, nb):
    try:
        identifiant=unroll_user_url(userurl)
        user = User.objects.get(id=identifiant)
    except:
        redirect('/accueil')

    try:
        articles = Article.objects.all().filter(auteur=user).order_by('-date') # Nous sélectionnons tous nos articles
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

    try:
        signature_object=Signature.objects.get(user=user)
        signature = signature_object.signature
        bio=signature_object.bio
        has_bio=True
        if len(bio)==0:
            has_bio=False
        if len(signature)<=5:
            signature = user.first_name+" "+user.last_name
    except:
        signature = user.first_name+" "+user.last_name
        has_bio=False
        bio=''

    return render(request, 'hiscolumns.html', {'user_search': user, 'signature':signature, 'has_bio':has_bio, 'bio':bio,'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':page_suiv, 'page_prec':page_prec, 'bool_suiv': bool_suiv, 'bool_prec': bool_prec})


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
        try:
            user_data=UserData.objects.all().filter(user=request.user)[0]
            user_data.number_articles=user_data.number_articles-1
            user_data.save()
        except:
            UserData(request.user).save()


    return redirect(reverse(userarticles_p0))

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profil.html', {
        'form': form
    })


@login_required
def savedarticles(request, nb):

    try:
        saved = Save.objects.all().filter(auteur=request.user).order_by('-date') # Nous sélectionnons tous nos articles
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