from django.urls import path
from . import views


urlpatterns = [

       path('', views.photoguide, name='photoguide'),
       path('<int:loc_id>', views.photoguide2, name='photoguide2'),
       path('photoguide_update/<int:loc_id>', views.photoguide_update, name='photoguide_update'),
       path('photoguide_result', views.photoguide_result, name='photoguide_result'),
       path('photoguide_result_copy', views.photoguide_result_copy, name='photoguide_result_copy'),

]
