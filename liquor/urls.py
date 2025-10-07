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
from utils import context_processors


urlpatterns = [
    path('cyberice/', admin.site.urls),
  

    path('',views.Index),
    path("login/", views.LoginView),
    path("logout/", views.LogoutView),
    path("register/", views.Register),
    path('searchby/',views.SearchBy),

    

    path('about/', views.About),
    path('termsofservice/',views.TermsOfService),
    path('privacy_and_policy/',views.PrivacyAndPolicy),
    
    path('shops/list/',views.ShopList),
    path('shops/create/',views.ShopCreate),
    path('shops/update/<int:pk>/', views.ShopUpdate),
    path('shops/delete/<int:pk>/',views.ShopDelete),
    path('shops/available/<int:pk>/',views.ShopAvailable),

    path('products/list/', views.ProductList),
    path('products/create/',views.ProductCreate),
    path('products/update/<int:pk>/', views.ProductUpdate),

    path('shoppingcart/list/',views.ShopCartList),
    path('shoppingcart/added/',views.ShopCartCreate),
    path('shoppingcart/update/<int:pk>/',views.ShopCartUpdate),
    path('shoppingcart/delete/<int:pk>/',views.ShopCartDelete),

    path("orders/list/", views.OrderList, name="orders_list"),
    path("orders/send/",views.OrderSend),
    path("orders/confirm/<int:pk>/", views.confirm_order, name="orders_confirm"),
    path("orders/<int:pk>/sell/", views.order_mark_sold, name="order_mark_sold"),

    path("account/profile/", views.profile_view, name="profile_view"),
    path(f"account/profilecus/<str:name>/", views.profile_view_cus),
    path("account/profile/edit/", views.profile_edit, name="profile_edit"),


    
    re_path(r'^.*/$', views.Custom404Page),
    
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
