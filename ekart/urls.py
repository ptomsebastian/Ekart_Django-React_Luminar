"""ekart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from eadmin import views
from eadmin.views import GetBookings, ProductByCategoryView, ProductDetailsView, ProductListView, RegisterCustomerAPIView, LoginCustomerAPIView, BookingsView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/customers/register/', RegisterCustomerAPIView.as_view(), name='register_customer'),
    path('api/customers/login/', LoginCustomerAPIView.as_view(), name='login_customer'),
    path('api/products/', ProductListView.as_view(), name='product-list'),
   path('api/products/<str:category>/', ProductByCategoryView.as_view(), name='product-by-category'),
   path('api/products/details/<int:product_id>/', ProductDetailsView.as_view(), name='product-details'),
    path('api/bookings/<int:product_id>/<int:customer_id>/', BookingsView.as_view(), name='bookings'),
    path('api/getbookings/<int:customer_id>/', GetBookings.as_view(), name='getbookings'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
