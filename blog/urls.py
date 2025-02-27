from django.urls import path
from django.conf import settings
from django.conf.urls.static import static    ## add for static files
from . import views


from .views import *

urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"), # modified
    path('article/<int:pk>', ArticleView.as_view(), name='article'),# new
    path('article/create', CreateArticleView.as_view(), name="create_article"), # new
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), ### NEW
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)