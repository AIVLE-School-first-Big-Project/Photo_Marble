from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.collection_mypage, name='collection'),
    path('ranking/', views.collection_ranking, name='ranking'),
    path('mygallery/', views.my_gallery, name='mygallery'),
    path('mygallery/<int:loc_id>/', views.my_gallery, name="my_gallery2"),
]