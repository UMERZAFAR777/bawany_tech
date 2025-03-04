"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from mysite import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('product/<slug:slug>',views.product_detail,name='product_detail'),
    path('error404/',views.error404,name='error404'),



    path('account/',views.account,name='account'),
    path('logout/',views.logout_user,name='handlelogout'),
    path('login/',views.login_user,name='handlelogin'),
    path('register',views.register,name='handleregister'),



    path('accounts/', include('django.contrib.auth.urls')),


    path('shop/',views.shop,name='shop'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),





    path('shop/filter-data',views.filter_data,name="filter-data"),


   


    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),


    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),


    path('wishlist/clear/', views.clear_wishlist, name='clear_wishlist'),

    path('checkout/',views.checkout,name='checkout'),
    # path('order_success/',views.order_success,name='order_success'),

    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    

    path("order_tracking/", views.order_tracking, name="order_tracking"),


    path("order_tracking/<int:order_id>/", views.order_tracking_detail, name="order_tracking_detail"),


]


if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

