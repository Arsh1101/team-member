from django.urls import path

from . import views
from django.urls import path


app_name = 'users'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]