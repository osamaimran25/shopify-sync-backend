# apps/product/urls.py

from django.urls import path

from apps.product.views.product_view import ProductListCreateAPIView, ProductDetailAPIView
from apps.product.webhooks.product_update_webhook import shopify_webhook

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<str:sku>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('webhook/shopify/', shopify_webhook, name='shopify-webhook'),
]
