from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
	path('variants/', views.variantlist, name='variant_list'),
    path('variant/new/', views.variant_new, name='variant_new'),
    ]