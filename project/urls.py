from django.urls import path
from django.conf import settings
from django.conf.urls.static import static    ## add for static files
from django.contrib.auth import views as auth_views
from . import views
from .views import RegisterView



urlpatterns = [ 
    path(r'', views.home, name="home"),
    path(r'user/<int:pk>', views.ShowUserPageView.as_view(), name="show_user"),
    path(r'posts', views.ShowAllPostsView.as_view(), name="show_all_posts"),
    path(r'post/<int:pk>', views.PostDetailView.as_view(), name="post_detail"),
    path(r'create_post', views.CreatePostView.as_view(), name="create_post"),
    path(r'post/<int:pk>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path(r'create_category', views.CreateCategoryView.as_view(), name="create_category"),
    path(r'login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
    path('post/<int:pk>/comment/', views.CreateCommentView.as_view(), name='create_comment'),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/repost/', views.toggle_repost, name='toggle_repost'),
    path('post/<int:post_id>/quote_repost/', views.create_quote_repost, name='create_quote_repost'),
    path('register/', RegisterView.as_view(), name='register'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('repost/<int:pk>/delete/', views.DeleteRepostView.as_view(), name='delete_repost'),
    path('messages/', views.inbox, name='inbox'),
    path('messages/new/', views.new_message, name='new_message'),
    path('messages/search/', views.search_users, name='search_users'),
    path('messages/<int:user_id>/', views.conversation, name='conversation'),
    path('user/<int:pk>/update/', views.UpdateUserProfileView.as_view(), name='update_profile'),
    path('edit-bio/', views.edit_bio, name='edit_bio'),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)