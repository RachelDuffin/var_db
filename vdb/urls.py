from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
	path('variants/', views.variantlist, name='variant_list'),
    path('login/', auth_views.LoginView.as_view(template_name='vdb/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='vdb/logout.html'), name = 'logout')

    ]