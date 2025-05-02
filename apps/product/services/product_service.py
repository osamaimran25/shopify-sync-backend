from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ValidationError

from apps.product.models import Product
from apps.product.serializers.product_serializer import ProductSerializer


class ProductService:
    @staticmethod
    @transaction.atomic
    def create_product(data: dict) -> Product:
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data
        product = Product.objects.create(
            name=validated['name'],
            sku=validated['sku'],
            price=validated['price'],
            quantity=validated['quantity'],
            last_updated=timezone.now()
        )
        return product

    @staticmethod
    @transaction.atomic
    def update_product(sku: str, data: dict) -> Product:
        try:
            product = Product.objects.get(sku=sku)
        except ObjectDoesNotExist:
            raise ValidationError(f"Product with SKU '{sku}' not found.")

        serializer = ProductSerializer(instance=product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        for attr, val in serializer.validated_data.items():
            setattr(product, attr, val)

        product.last_updated = timezone.now()
        product.save()

        return product

    @staticmethod
    @transaction.atomic
    def delete_product(sku: str) -> None:

        try:
            product = Product.objects.get(sku=sku)
        except ObjectDoesNotExist:
            raise ValidationError(f"Product with SKU '{sku}' not found.")
        product.delete()

    @staticmethod
    def get_product(sku: str) -> Product:
        try:
            return Product.objects.get(sku=sku)
        except ObjectDoesNotExist:
            raise ValidationError(f"Product with SKU '{sku}' not found.")

    @staticmethod
    def filter_products(
        name: str = None,
        sku: str = None,
        price: Decimal = None,
        quantity: int = None
    ):
        qs = Product.objects.all()
        if name is not None:
            qs = qs.filter(name__icontains=name)
        if sku is not None:
            qs = qs.filter(sku__icontains=sku)
        if price is not None:
            qs = qs.filter(price=price)
        if quantity is not None:
            qs = qs.filter(quantity=quantity)
        return qs
