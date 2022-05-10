from django.urls import *
from . import views


urlpatterns = [
    # main
    path('', views.main, name='main'),

    # login
    path('login/', views.login, name='login'),

    # mypage
    path('mypage/', views.mypage, name='mypage'),
    path('mypage/profile_upload', views.profile_upload, name="profile_upload"),

    # 회원탈퇴
    path('mypage/delete/', views.delete, name='delete'),
    path('delete_account/', views.delete_account, name="delete_account"),
    path('delete/', views.delete, name="delete"),
    path('delete_result/', views.delete_result, name="delete_result"),

    # 회원가입
    path('signup/', views.CustomSignupView.as_view(), name="custom_signup"),

    # 로그아웃
    path('logout/', views.CustomSLogoutView.as_view(), name="custom_logout"),

    # 패스워드 변경
    path('password/change/', views.CustomSPasswordChangeView.as_view(), name="custom_pc"),

    # 이메일 인증
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    path('signup3/', views.signup3, name='signup3'),

    # About PhotoMarble (포토마불 사용가이드)
    path('about_pm/', views.about_pm, name='about_pm'),
]
