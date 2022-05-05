from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.collection_mypage, name='collection'),
    path('ranking/', views.collection_ranking, name='ranking'),
    path('mygallery/', views.my_gallery_tmp, name='my_gallery'),
    path('map_modal/', views.map_modal, name='map_modal'),
    path('collection_modal/', views.collection_modal, name='collection_modal'),
    path('mygallery/<int:loc_id>/', views.my_gallery, name="my_gallery2"),
    path('collection_update', views.collection_update, name='collection_update'),

]