from django.urls import path
from . import views

urlpatterns = [

    path('', views.store, name='store'),
    path('class/<slug:classification_slug>/', views.store, name='products_by_class'),
    path('class/<slug:classification_slug>/<slug:product_slug>/', views.product_detail, name='products_detail'),
    path('search/', views.search, name='search'),

]
