from django.urls import path, include
from . import views
urlpatterns = [

    path('collection/', views.collection_mypage, name='collection'),
    path('ranking/', views.collection_ranking, name='ranking'),

]