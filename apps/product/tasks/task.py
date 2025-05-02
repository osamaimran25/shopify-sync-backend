from celery import shared_task
import csv
from django.core.mail import send_mail
from django.conf import settings

from apps.product.services.product_service import ProductService


@shared_task
def import_products_from_csv():
    path = settings.BASE_DIR / 'mock_data.csv'
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ProductService.update_product(sku=row['sku'], quantity=int(row['quantity']))
            except ValueError:
                # skip missing products
                continue
    validate_and_report.delay()

@shared_task
def validate_and_report():
    # Simplified report logic
    subject = 'Nightly Inventory Report'
    message = 'Inventory import completed successfully.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=False)
