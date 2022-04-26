from django.urls import path, include
from . import views
urlpatterns = [
       path('', views.photoguide, name='photoguide'),
       path('photoguide_update', views.photoguide_update, name='photoguide_update'),

]