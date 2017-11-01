from articles.models import Article
from datetime import date, datetime
from numpy import exp

def process_ranking_all():
	articles = Article.objects.all()
	for i in range(len(articles)):
		article=articles[i]
		publication=article.date
		now = datetime.now()
		duration=now-publication.replace(tzinfo=None)
		article.ranking=1000*(article.likes*0.1+1)*exp(-duration.days/7)
		article.save()

def process_ranking(id):
	article = Article.objects.get(id=id)
	publication=article.date
	now = datetime.now()
	duration=now-publication.replace(tzinfo=None)
	article.ranking=1000*(article.likes*0.1+1)*exp(-duration.days/7)
	article.save()