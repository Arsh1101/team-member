from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'users'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('add', views.AddMemberView.as_view(), name='add'),
    # path('edit/<int:pk>', views.EditMemberView.as_view(), name='edit'),
    # path('delete/<int:pk>', views.DeleteMemberView.as_view(), name='delete'),
    path('add', login_required(views.AddMemberView.as_view()), name='add'),
    path('edit/<int:pk>', login_required(views.EditMemberView.as_view()), name='edit'),
    path('delete/<int:pk>', login_required(views.DeleteMemberView.as_view()), name='delete'),
    # path('', views.login_page, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
]