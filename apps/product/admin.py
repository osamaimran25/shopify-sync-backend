from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'quantity', 'last_updated')
    search_fields = ('name', 'sku')
    list_filter = ('last_updated',)
    actions = ['bulk_update_price']

    def bulk_update_price(self, request, queryset):
        for product in queryset:
            product.price += 1  # simplistic logic for example
            product.save()
        self.message_user(request, "Prices updated successfully.")
