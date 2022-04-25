from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.gallery, name="select"),
    path('detail/<int:id>/', views.detail, name="detail2"),
    path('detail/comment/delete/<int:g_id>/<int:c_id>',views.comment_delete, name='comment_delete')
]
