from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),	
    path('variants/', views.variantlist, name='variant_list'),
    path('variants/<int:pk>/', views.variantviewer, name='variant_viewer'),
    path('variants/new/', views.variant_new, name='variant_new'),
  
    # authentication pages
    path('login/', auth_views.LoginView.as_view(template_name='vdb/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='vdb/logout.html'), name = 'logout'),
    path('login/password_reset/', auth_views.PasswordResetView.as_view(template_name='vdb/password_reset.html'), name = 'password_reset'),
    path('login/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='vdb/password_reset_done.html'), name = 'password_reset_done'),

    # variant pages
    path('variants/', views.variantlist, name='variant_list'),
    path('variants/<int:pk>/', views.variantviewer, name='variant_viewer')
    ]