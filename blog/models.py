from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    '''Encapsulate the idea of a Article by some author.'''

    # data attributes of a Article:
    title = models.TextField(blank=False)
    text = models.TextField(blank=False)
    author = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) ## NEW

    #image_url = models.URLField(blank=True) # url as a string
    image_file = models.ImageField(blank=True) # an actual image
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        return reverse('article',kwargs={'pk':self.pk})
    
    def get_all_comments(self):
        comments = Comment.objects.filter(article=self)
        return comments

    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text}'
        