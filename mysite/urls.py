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
]


if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

