from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new/", views.new_page, name= "new_page"),
    path("randompage/", views.randompage, name="randompage"),
    path("search/", views.search, name="search")
   
    
]   
 