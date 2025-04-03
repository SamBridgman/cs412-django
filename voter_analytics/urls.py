from django.urls import path
from .views import VoterListView, VoterGraphsView, VoterDetailView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('graphs/', VoterGraphsView.as_view(), name='graphs'),
    path('voter/<str:pk>/', VoterDetailView.as_view(), name='voter'),
] 