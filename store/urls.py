from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('<slug:classification_slug>/', views.store, name='products_by_class'),
    path('<slug:classification_slug>/<slug:product_slug>/', views.product_detail, name='products_detail'),

]
