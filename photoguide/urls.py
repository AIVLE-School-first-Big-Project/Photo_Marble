from django.urls import path
from . import views


urlpatterns = [
       # 포토가이드 화면
       path('<int:loc_id>', views.photoguide2, name='photoguide2'),

       # 포토가이드 사진 업로드 및 결과
       path('photoguide_update/<int:loc_id>', views.photoguide_update, name='photoguide_update'),
       path('photoguide_result', views.photoguide_result, name='photoguide_result'),

]
