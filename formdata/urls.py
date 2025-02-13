from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.main, name="main"),
    path(r'confirmaton', views.confirmtion, name="confirmation"), 
    path(r'order', views.order, name="order"), 
]
