from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('task/add/', views.task_create, name='task_add'),
    path('task/<int:pk>/edit/', views.task_update, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
]
