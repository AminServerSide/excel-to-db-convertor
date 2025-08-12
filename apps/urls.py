from django.urls import path
from . import views

app_name = 'apps'

urlpatterns = [
    path('upload/', views.upload_excel, name='upload_excel'),
]