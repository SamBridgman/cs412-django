from django.urls import path
from django.conf import settings
from django.conf.urls.static import static    ## add for static files
from . import views
from .views import ShowAllView # our view class definition 



urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllView.as_view(), name='show_all'), # generic class-based view
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)