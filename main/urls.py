from django.urls import *
from . import views
urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/delete/', views.delete, name='delete'),
    path('', views.main, name='main'),
    path('main/', views.main, name='main'),
    # path('signup/', views.SignupView, name="account_signup"),   
    path('signup/', views.CustomSignupView.as_view(), name="custom_signup"),     
    path('logout/', views.CustomSLogoutView.as_view(), name="custom_logout"),   
]