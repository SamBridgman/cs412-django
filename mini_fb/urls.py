from django.urls import path
from django.conf import settings
from django.conf.urls.static import static    ## add for static files
from . import views

from .views import *

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="ShowAllProfilesView"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),# new
    path('create_profile', CreateProfileView.as_view(), name="create_profile"), # new
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status')
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)