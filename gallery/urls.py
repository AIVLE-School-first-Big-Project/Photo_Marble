from django.urls import path, include
from . import views
from .views import Detail

#app_name = 'gallery'

urlpatterns = [
    path('select/', views.select, name="select"),
    path('detail/', Detail.as_view()),
    path('detail/<int:id>', Detail.as_view()),
]
