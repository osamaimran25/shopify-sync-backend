
from decimal import Decimal
import re

from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.product.models import Product

SKU_REGEX = re.compile(r'^[A-Z0-9_-]{3,20}$')

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        allow_blank=False,
        trim_whitespace=True,
    )
    sku = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(queryset=Product.objects.all(), message="SKU already exists."),
        ]
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.00'),
        error_messages={
            "min_value": "Price must be zero or a positive amount.",
        }
    )
    quantity = serializers.IntegerField(
        min_value=0,
        error_messages={
            "min_value": "Quantity cannot be negative.",
        }
    )
    last_updated = serializers.DateTimeField(read_only=True)

    def validate_name(self, value: str) -> str:
        # no all-numeric names
        if value.isdigit():
            raise serializers.ValidationError("Name must contain alphabetic characters.")
        return value

    def validate_sku(self, value: str) -> str:
        # enforce format: uppercase letters, numbers, underscores or hyphens, 3–20 chars
        if not SKU_REGEX.match(value):
            raise serializers.ValidationError(
                "SKU must be 3–20 characters: uppercase letters, digits, '_' or '-'."
            )
        return value

    def validate_price(self, value: Decimal) -> Decimal:
        # ensure at most two decimal places
        if value.quantize(Decimal('0.01')) != value:
            raise serializers.ValidationError("Price must have at most two decimal places.")
        return value

    def validate_quantity(self, value: int) -> int:
        # disallow extremely large inventories
        if value > 10_000:
            raise serializers.ValidationError("Quantity seems unreasonably large.")
        return value

    def validate(self, data: dict) -> dict:
        # cross-field: if price is zero, quantity must also be zero
        price = data.get('price')
        qty   = data.get('quantity')
        if price == Decimal('0.00') and qty and qty > 0:
            raise serializers.ValidationError(
                "Cannot have a positive quantity when price is zero."
            )
        return data
