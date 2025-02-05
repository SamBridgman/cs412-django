from django.urls import path
from django.conf import settings
from django.conf.urls.static import static    ## add for static files
from . import views



urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.quote, name="quote_page"),
    path(r'quote', views.quote, name="quote_page"),
    path(r'show_all', views.show_all, name="show_all_page"),
    path(r'about', views.about, name="about_page"),

] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)