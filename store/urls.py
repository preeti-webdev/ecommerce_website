from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.register, name='register'),
    path( 'login/',auth_views.LoginView.as_view(template_name='store/login.html'),name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('place-order/',views.place_order,name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('update-cart/<int:id>/',views.update_cart, name='update_cart'),
    path('remove-cart/<int:id>/',views.remove_from_cart,name='remove_from_cart'),
    path('add-to-wishlist/<int:id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),

]