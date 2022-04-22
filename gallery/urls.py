from django.urls import path, include
from . import views


# app_name = 'gallery'

urlpatterns = [
    path('', views.gallery, name="select"),
    path('detail/<int:id>/', views.detail, name="detail"),

]
