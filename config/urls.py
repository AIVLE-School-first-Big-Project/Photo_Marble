"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
from main.views import CustomPasswordChangeView
urlpatterns = [
    #admin
    path('admin/', admin.site.urls),
    #main
    path('', include('main.urls')),

    #allauth
    path("email-confirmation-done/",
        TemplateView.as_view(template_name="main/email-confirmation-done.html"),
        name="account_email_confirmation_done"),
    path('password/change/', CustomPasswordChangeView.as_view(), name="account_change_password"),
    path('',include('allauth.urls')),
]
