# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from django.core.urlresolvers import reverse
from process_ranking import *
import unicodedata
from google_analytics import initialize_analyticsreporting, get_report
# Create your views here.

from articles.models import Article, Categorie, Comment, Like, Save, Signature
import tweepy
from tweepy import OAuthHandler

from twitter_keys import *
import re
import operator


emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

http_str = [
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
]
    
tokens_http_re = re.compile(r'('+'|'.join(http_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize_http(s):
    return tokens_http_re.findall(s)
 
def find_links(s, lowercase=False):
    tokens = tokenize_http(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def get_id(url):
    return url.split('-')[-1]

def get_url(article):
    url='user/'
    url=url+article.auteur.username.lower()+'/'
    url=url+unicodedata.normalize('NFKD',  article.titre.lower()).encode('ascii', 'ignore').replace(',','').replace('?','').replace('!','').replace('(','').replace(')','').replace('$','').replace('#','').replace('@','').replace('%','').replace('#','').replace('(','').replace(')','').replace(';','').replace('/','').replace(':','').replace("'",'-').replace("\"",'').replace(' ','-')+'-'
    url=url+str(article.id)
    return url

def homepage(request):
    return redirect('/accueil')

def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    articles = Article.objects.order_by('-ranking') # Nous sélectionnons tous nos articles

    if len(articles)>10:
        n=5
        bool_suiv=True
    else:
        n=int(len(articles)/2)
        bool_suiv=False

    articles1=[]
    articles2=[]
    for i in range(n):
        articles1.append(articles[2*i])
        articles2.append(articles[2*i+1])

    if len(articles)<10 and 2*int(len(articles)/2) != len(articles):
        articles1.append(articles[len(articles)-1])
    
    bool_prec=False

    return render(request, 'blog/accueil.html', {'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':1, 'page_prec':0,'bool_suiv': bool_suiv, 'bool_prec': bool_prec})

def read_page(request, nb):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    articles = Article.objects.order_by('-ranking') # Nous sélectionnons tous nos articles
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
        articles = Article.objects.order_by('-ranking').filter(categorie=categorie) # Nous sélectionnons tous nos articles
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

    return render(request, 'blog/accueil.html', {'tag': id, 'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':page_suiv, 'page_prec':page_prec, 'bool_suiv': bool_suiv, 'bool_prec': bool_prec})

def search(request, phrase):
    return search_page(request, phrase, 0)

def search_form(request):
    if request.method == 'POST':
        search_arg = request.POST.get('search')
        return search(request, search_arg)
    else:
        return redirect('/accueil')

def search_page(request, phrase, nb):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    try:
        cursor = connection.cursor()
        words=phrase.split(" ")
        print(words)
        sql="SELECT id FROM articles_article WHERE "
        for i in words:
            sql=sql+"(contenu LIKE '%"+str(i)+"%' OR titre LIKE '%"+str(i)+"%' OR sous_titre LIKE '%"+str(i)+"%') AND "
        sql=sql[:-5]+" ORDER BY ranking DESC"
        print(sql)
        cursor.execute(sql)
        articles_id = cursor.fetchall() # Nous sélectionnons tous nos articles
        print(articles_id)
        articles=[]
        for i in articles_id:
            print(i)
            art=Article.objects.get(id=i[0])
            articles.append(art)
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

    return render(request, 'blog/articles_on_search.html', {'search': phrase, 'derniers_articles_1': articles1,'derniers_articles_2': articles2, 'page_suiv':page_suiv, 'page_prec':page_prec, 'bool_suiv': bool_suiv, 'bool_prec': bool_prec})


def read_by_tag_p0(request, id):
    return read_by_tag(request, id, 0)

def get_article(request, user, article_url):
    id=get_id(article_url)
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404
    else:
        return lire(request,id)

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
        signature_object=Signature.objects.get(user=article.auteur)
        signature = signature_object.signature
        bio=signature_object.bio
        has_bio=True
        if len(bio)==0:
            has_bio=False
        if len(signature)<=5:
            signature = article.auteur.first_name+" "+article.auteur.last_name
    except:
        signature = article.auteur.first_name+" "+article.auteur.last_name
        has_bio=False
        bio=''

    if len(signature)<=5:
        signature = article.auteur.username


    return render(request, 'blog/lire.html', {'article': article, 'form':form, 'comments': comments, 'has_liked':has_liked, 'number_of_likes':number_of_likes,'signature':signature, 'has_bio':has_bio, 'bio':bio})

class table_row():
    def __init__(self, v1,v2):
        self.value1=v1
        self.value2=v2

class twitter_trend():
    def __init__(self, hashtag,link,volume):
        self.hashtag=hashtag
        self.link=link
        self.volume=volume
        self.clean_hashtag=hashtag.replace('#','')

@login_required
def tweets(request):
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        trends=(api.trends_place(23424819))
        trends=trends[0]['trends']
        trends_list=[]
        for i in trends:
            if type(i['tweet_volume'])==int:
                volume=str(i['tweet_volume'])
            else:
                volume=''
            trends_list.append(twitter_trend(i['name'], i['url'], volume))
        return render(request, 'blog/twitter.html', {'trends': trends_list})
    except:
        return redirect(reverse(home))


class twitter_link():
    def __init__(self, link, retweets, title, media_link):
        self.link=v1
        self.retweets=retweets
        self.title=v2
        self.media_link=v2

@login_required
def tweets_analyze(request, hashtag):
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        trends=(api.trends_place(23424819))
        data=[]
        text_data={}
        text_data_preprocessed=[]
        links={}
        links_media={}
        links_title={}
        for status in tweepy.Cursor(api.search, q=hashtag).items(50):
            # Process a single status
            data.append(status)
            text_data[status.text]=status._json['retweet_count']
            preprocess_text=preprocess(status.text)
            preprocess_text_cleaned=[]
            for i in status.text_json['entities']['media']:
                links[i["expanded_url"]]=status._json['retweet_count']
                links_media[i["expanded_url"]]=i["media_url"]
                links_title[i["expanded_url"]]=status.text
                print("OK")
            for i in preprocess_text:
                if len(i)>2:
                    preprocess_text_cleaned.append(i.lower())
            text_data_preprocessed.append(preprocess_text_cleaned)

        frequencies={}
        for i in text_data_preprocessed:
            for j in i:
                if j not in frequencies:
                    frequencies[j]=1
                else:
                    frequencies[j]=frequencies[j]+1

        print("Step 1")
        frequencies_sorted=sorted(frequencies.items(), key=operator.itemgetter(1))
        frequencies_sorted.reverse()

        text_data_sorted=sorted(text_data.items(), key=operator.itemgetter(1))
        text_data_sorted.reverse()

        tweets=[]
        for i in text_data_sorted:
            tweets.append(table_row(i[0],i[1]))

        links_sorted=sorted(links.items(), key=operator.itemgetter(1))
        links_sorted.reverse()

        print("Step 2")
        links_table=[]
        for i in links_sorted:
            links_table.append(twitter_link(i[0], i[1], links_media[i[0]], links_title[i[0]]))

        print("Step 3")
        frequencies_table=[]
        for i in range(10):
            frequencies_table.append(table_row(frequencies_sorted[i][0],str(frequencies_sorted[i][1])))
        
        print("Step 4")
        return render(request, 'blog/twitter_analyze.html', {'hashtag': hashtag, 'data': tweets, 'frequencies':frequencies_table, 'links':links_table})
    except:
        return redirect(reverse(home))

@login_required
def metrics(request, id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404

    if article.auteur==request.user:
        try:
            likes = Like.objects.all().filter(article=article)
            number_of_likes=len(likes)
        except:
            number_of_likes=0
        
        try:
            comments=Comment.objects.all().filter(article=article)
            nb_comments=len(comments)
        except:
            comments=[]
            nb_comments=0

        analytics = initialize_analyticsreporting()
        report=get_report(analytics)
        personal_report_dim=[]
        personal_report=[]
        temps_moyen=0
        sources={}
        medium={}
        cities={}
        for i in range(len(report['reports'][0]['data']['rows'])):
            if get_id(report['reports'][0]['data']['rows'][i]['dimensions'][5])==id:
                personal_report_dim.append(report['reports'][0]['data']['rows'][i]['dimensions'])
                personal_report.append(report['reports'][0]['data']['rows'][i]['metrics'][0]['values'])
                temps_moyen=temps_moyen+float(report['reports'][0]['data']['rows'][i]['metrics'][0]['values'][3])
                if report['reports'][0]['data']['rows'][i]['dimensions'][1] not in sources:
                    sources[report['reports'][0]['data']['rows'][i]['dimensions'][1]]=1
                else:
                    sources[report['reports'][0]['data']['rows'][i]['dimensions'][1]]=sources[report['reports'][0]['data']['rows'][i]['dimensions'][1]]+1
                if report['reports'][0]['data']['rows'][i]['dimensions'][2] not in medium:
                    medium[report['reports'][0]['data']['rows'][i]['dimensions'][2]]=1
                else:
                    medium[report['reports'][0]['data']['rows'][i]['dimensions'][2]]=medium[report['reports'][0]['data']['rows'][i]['dimensions'][2]]+1
                if report['reports'][0]['data']['rows'][i]['dimensions'][4] not in cities:
                    cities[report['reports'][0]['data']['rows'][i]['dimensions'][4]]=1
                else:
                    cities[report['reports'][0]['data']['rows'][i]['dimensions'][4]]=cities[report['reports'][0]['data']['rows'][i]['dimensions'][4]]+1
        if (len(personal_report)>0):
            temps_moyen=int(temps_moyen/len(personal_report))
        else:
            temps_moyen=0
        table_sources=[]
        for i in sources:
            table_sources.append(table_row(i,sources[i]))
        table_medium=[]
        for i in medium:
            table_medium.append(table_row(i,medium[i]))
        table_cities=[]
        for i in cities:
            table_cities.append(table_row(i,cities[i]))
        return render(request, 'blog/analytics.html', {'article': article,'table_medium': table_medium, 'table_cities':table_cities, 'table_sources': table_sources, 'report':personal_report, 'vues':len(personal_report), 'temps_moyen':temps_moyen, 'report_dim': personal_report_dim, 'number_of_comments':nb_comments, 'number_of_likes':number_of_likes})
    else:
        return redirect(reverse(home))


@login_required
def new(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    if request.method=="POST":
        form = ArticleForm(request.POST, request.FILES)
            # Nous vérifions que les données envoyées sont valides
            # Cette méthode renvoie False s'il n'y a pas de données 
            # dans le formulaire ou qu'il contient des erreurs.
        if form.is_valid(): 
                # Ici nous pouvons traiter les données du formulaire
            new_article=Article()
            new_article.auteur=request.user
            new_article.titre = form.cleaned_data.get('titre')
            new_article.contenu = form.cleaned_data.get('contenu')
            new_article.sous_titre = form.cleaned_data.get('sous_titre')
            new_article.categorie = form.cleaned_data.get('categorie')
            new_article.photo = form.cleaned_data['photo']
            new_article.save()
            new_article.url = get_url(new_article)
            new_article.time_to_read=int(float(len(new_article.contenu.split(' '))/200))+1
            new_article.save()

                # Nous pourrions ici envoyer l'e-mail grâce aux données 
                # que nous venons de récupérer
            envoi = True
            process_ranking_all()
    else:
        form = ArticleForm(None)
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
        article.likes=article.likes-1
        article.save()
        process_ranking(id)
    else:
        new_like=Like()
        new_like.auteur=request.user
        new_like.article = article
        new_like.save()
        article.likes=article.likes+1
        article.save()
        process_ranking(id)
    return redirect('/article/'+id)

@login_required
def actualize_rank(request):
    process_ranking_all()
    return redirect('/accueil')

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