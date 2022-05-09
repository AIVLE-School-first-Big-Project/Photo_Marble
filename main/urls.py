from django.urls import *
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/delete/', views.delete, name='delete'),
    path('', views.main, name='main'),
    path('signup/', views.CustomSignupView.as_view(), name="custom_signup"),
    path('logout/', views.CustomSLogoutView.as_view(), name="custom_logout"),
    path('password/change/', views.CustomSPasswordChangeView.as_view(), name="custom_pc"),
    path('delete_account/', views.delete_account, name="delete_account"),
    path('delete/', views.delete, name="delete"),
    path('delete_result/', views.delete_result, name="delete_result"),
    path('mypage/profile_upload', views.profile_upload, name="profile_upload"),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    path('signup3/', views.signup3, name='signup3'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('about_pm/', views.about_pm, name='about_pm'),
]
