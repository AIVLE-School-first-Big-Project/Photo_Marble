from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
from main.views import CustomPasswordChangeView
urlpatterns = [
    #admin
    path('admin/', admin.site.urls),
    #main
    path('', include('main.urls')),
    path('collection/', include('collection.urls')),
    #allauth
    path("email-confirmation-done/",
        TemplateView.as_view(template_name="main/email-confirmation-done.html"),
        name="account_email_confirmation_done"),
    path('password/change/', CustomPasswordChangeView.as_view(), name="account_change_password"),
    path('', include('allauth.urls')),
    path('', include('gallery.urls')),
]
