# coding: utf-8
from django import forms
from .models import Article, Comment

class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse mail", widget=forms.TextInput(attrs={'class' : 'form-control'}))
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)

    def clean_message(self):
        message = self.cleaned_data['message']
        if "pizza" in message:
            raise forms.ValidationError("On ne veut pas entendre parler de pizza !")

        return message

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields=('titre','contenu','categorie',)
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': '20'}),
        }
        #fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('contenu',)
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
        }
        #fields = '__all__'