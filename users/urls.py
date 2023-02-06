from django.urls import path

from . import views
from django.urls import path


app_name = 'users'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add', views.AddMemberView.as_view(), name='add'),
    path('edit/<int:pk>', views.EditMemberView.as_view(), name='edit'),
    path('delete/<int:pk>', views.DeleteMemberView.as_view(), name='delete'),
]