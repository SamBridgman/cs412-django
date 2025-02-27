from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    "A form to add an article to db"
    class Meta:
        "assosciate this form wit a model in a db"
        model = Article
        fields = ['author','title','text','image_url']

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''

    class Meta:
        '''associate this form with the Comment model; select fields'''
        model = Comment
        fields = ['author', 'text', ]  # which fields from model should we use
