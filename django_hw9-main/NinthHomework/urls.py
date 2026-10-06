from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.reports_dashboard, name='reports_dashboard'),
    
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
]