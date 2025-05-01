from django.contrib import admin
from .models import Post, Category, Comment, Like, Repost, Message, UserProfile

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Repost)
admin.site.register(Message)
admin.site.register(UserProfile)