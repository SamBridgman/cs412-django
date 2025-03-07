from django.urls import path
from django.conf import settings
from django.conf.urls.static import static    ## add for static files
from . import views

from .views import *

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="ShowAllProfilesView"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),# new
    path('create_profile', CreateProfileView.as_view(), name="create_profile"), # new
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name ='delete'),
    path("status/<int:pk>/update", UpdateStatusMessageView.as_view(), name='update_status')
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)