from articles.models import Article
from datetime import date
from numpy import exp

def process_ranking_all():
	articles = Article.objects.all()

def process_ranking(id):
	article = Article.objects.get(id=id)
	publication=article.date
	now = datetime.now()
	duration=now-publication
	article.ranking=(article.likes/10+1)*exp(-duration.days/7)
	article.save()