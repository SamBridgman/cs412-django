from django.urls import path
from django.conf import settings
from django.conf.urls.static import static    ## add for static files
from . import views
from django.contrib.auth import views as auth_views    ## NEW


from .views import *

urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"), # modified
    path('article/<int:pk>', ArticleView.as_view(), name='article'),# new
    path('article/create', CreateArticleView.as_view(), name="create_article"), # new
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), ### NEW
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"), # NEW
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),  ## NEW
    # path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'), ## NEW
	# path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), ## NEW
    # path('register/', RegistrationView.as_view(), name='register'),


]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)