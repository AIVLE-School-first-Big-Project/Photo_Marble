from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/delete', views.delete, name='account_delete'),

]