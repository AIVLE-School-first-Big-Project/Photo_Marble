from django.urls import *
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('', views.main, name='main'),#경주
    path('main/', views.main, name='main'),
    # path('signup/', views.SignupView, name="account_signup"),
    path('signup2/', views.CustomSignupView.as_view(), name="custom_signup"),
    path('gallery/', views.gallery, name='main'),
]