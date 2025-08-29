"""
URL configuration for liquor project.

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
from django.urls import path, re_path
from liquorapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
  

    path('',views.Index),
    path("login/", views.LoginView),
    path("logout/", views.LogoutView),
    path("register/", views.Register),

    path('about/', views.About),

    
    path('shops/list/',views.ShopList),
    path('shops/create/',views.ShopCreate),

    path('products/list/', views.ProductList),
    path('products/create/',views.ProductCreate),

    path('shoppingcart/',views.ShopCartList),
    path('shoppingcart/added/',views.ShopCartCreate),

    path('termofservice/',views.TermOfService),
    re_path(r'^.*/$', views.Custom404Page),
    
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
