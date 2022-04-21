from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('main/', views.main, name='main'),#경주
    path('signup/', views.CustomSignupView.as_view(), name="account_signup"),
]