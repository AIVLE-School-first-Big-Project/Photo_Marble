from django.urls import path, include
from . import views


#app_name = 'gallery'

urlpatterns = [
    path('select/', views.select, name="select"),
    path('detail/', views.detail, name="detail"),
    path('detail/<int:id>', views.detail, name="detail2"),
]
