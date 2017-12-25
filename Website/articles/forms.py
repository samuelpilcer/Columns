# coding: utf-8
from django import forms
from mediumeditor_fork.widgets import MediumEditorTextarea
from .models import Article, Comment, Fil, InFil


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
        fields=('photo','titre','sous_titre','contenu','categorie',)
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder':'Titre','class': 'form-control'}),
            'sous_titre': forms.TextInput(attrs={'placeholder':"Phrase d'accroche",'class': 'form-control'}),
            'contenu':  MediumEditorTextarea(),
            #'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': '20'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={"class":"btn btn-primary btn-file"}),

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

class AddToFilForm(forms.ModelForm):
    class Meta:
        model = InFil
        fields=('id',)
        widgets = {
            'id': forms.IntegerField(label='Identifiant'),
        }
        #fields = '__all__'

class FilForm(forms.ModelForm):
    class Meta:
        model = Fil
        fields=('photo','nom','description',)
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder':'Titre','class': 'form-control'}),
            'description':  MediumEditorTextarea(),
            'photo': forms.FileInput(attrs={"class":"btn btn-primary btn-file"}),

        }
        #fields = '__all__'