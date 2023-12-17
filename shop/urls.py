from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<int:id>/', views.detail, name='detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-item/<int:product_id>/', views.add_to_cart, name='add-item'),
    path('del-item/<int:product_id>/', views.delete_from_cart, name='del-item'),
    path('checkout/', views.checkout, name='checkout'),
]