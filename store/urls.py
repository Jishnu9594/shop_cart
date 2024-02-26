from django.urls import path
from  . import views


urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('cart/<int:productId>/', views.cart, name='cart'),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login, name="login"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="update_item"),

]