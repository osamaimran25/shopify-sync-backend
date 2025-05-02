# webhook.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from apps.product.services.product_service import ProductService


@api_view(['POST'])
@permission_classes([AllowAny])
def shopify_webhook(request):
    data = request.data
    sku = data.get('sku')
    quantity = data.get('quantity')
    if not sku or quantity is None:
        return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        ProductService.update_product(sku=sku, quantity=int(quantity))
        return Response({'message': 'Inventory updated'})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
