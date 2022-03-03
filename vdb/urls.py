from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
	path('variants/', views.variantlist, name='variant_list'),
    path('variants/new/', views.variant_new, name='variant_new'),
    path('gene/new/', views.gene_new, name='gene_new')

    ]