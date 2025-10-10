from django.urls import path
from .views import RegisterView, home, login_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', login_view, name='logout'),
    path('', home, name='home'),
]