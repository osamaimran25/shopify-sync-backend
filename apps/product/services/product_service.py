from django.db import transaction
from .models import Product
from django.core.exceptions import ObjectDoesNotExist

class ProductService:
    @staticmethod
    def create_product(name: str, sku: str, price: float, quantity: int) -> Product:
        return Product.objects.create(
            name=name,
            sku=sku,
            price=price,
            quantity=quantity
        )

    @staticmethod
    def update_product(sku: str, **kwargs) -> Product:
        try:
            product = Product.objects.get(sku=sku)
            for attr, value in kwargs.items():
                setattr(product, attr, value)
            product.save()
            return product
        except ObjectDoesNotExist:
            raise ValueError("Product not found")

    @staticmethod
    def delete_product(sku: str) -> None:
        try:
            product = Product.objects.get(sku=sku)
            product.delete()
        except ObjectDoesNotExist:
            raise ValueError("Product not found")

    @staticmethod
    def filter_products(name: str = None, sku: str = None, price: float = None, quantity: int = None):
        queryset = Product.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        if sku:
            queryset = queryset.filter(sku__icontains=sku)
        if price is not None:
            queryset = queryset.filter(price=price)
        if quantity is not None:
            queryset = queryset.filter(quantity=quantity)
        return queryset
