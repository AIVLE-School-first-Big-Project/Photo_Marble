from django.urls import path
from . import views

urlpatterns = [

    # 컬렉션 기본페이지
    path('', views.collection_mypage, name='collection'),

    # 랭킹 페이지
    path('ranking/', views.collection_ranking, name='ranking'),

    # 나의 갤러리
    path('mygallery/<int:loc_id>/', views.my_gallery, name="my_gallery2"),

    # 서울 지역구 활성화시 모달
    path('map_modal/', views.map_modal, name='map_modal'),
    path('collection_modal/', views.collection_modal, name='collection_modal'),

    # 객체 인식
    path('collection_update', views.collection_update, name='collection_update'),
]
