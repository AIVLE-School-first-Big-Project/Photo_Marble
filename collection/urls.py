from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.collection_mypage, name='collection'),
    path('ranking/', views.collection_ranking, name='ranking'),
    path('mygallery/', views.my_gallery, name='mygallery'),
]