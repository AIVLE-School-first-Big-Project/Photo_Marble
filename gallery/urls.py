from django.urls import path
from . import views


urlpatterns = [

    # 갤러리 기본페이지
    path('', views.gallery, name="gallery"),

    # 사진 상세페이지 좋아요 기능
    path('detail/likes', views.likes, name='likes'),

    # 사진 업로드
    path('upload', views.upload, name="upload"),

    # 사진 상세페이지 (단일 Feed)
    path('detail/<int:id>/', views.detail, name="detail2"),

    # Feed 삭제
    path('detail/comment/delete/<int:g_id>/<int:c_id>', views.comment_delete, name='comment_delete'),

    # Pagination
    path('load_more/', views.load_more, name="load_more"),
    path('detail/gallery/delete/<int:g_id>', views.gallery_delete, name='gallery_delete')
]
