from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
	path('variants/', views.variantlist, name='variant_list')

    ]