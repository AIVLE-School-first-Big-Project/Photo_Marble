from django.urls import path, include
from . import views


urlpatterns = [
    path('detail/likes', views.likes, name='likes'),
    path('', views.gallery, name="gallery"),
    path('upload', views.upload, name="upload"),
    path('detail/<int:id>/', views.detail, name="detail2"),
    path('detail/comment/delete/<int:g_id>/<int:c_id>',views.comment_delete, name='comment_delete'),

    # Pagination
    path('list/', views.gallery_list, name="gallery_list"),

]
