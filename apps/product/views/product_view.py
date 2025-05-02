from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.product.models import Product
from apps.product.services import ProductService


class ProductListCreateAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = {
            'name': request.query_params.get('name'),
            'sku': request.query_params.get('sku'),
            'price': request.query_params.get('price'),
            'quantity': request.query_params.get('quantity'),
        }
        products = ProductService.filter_products(**{k: v for k, v in filters.items() if v is not None})
        data = [{
            'name': p.name,
            'sku': p.sku,
            'price': float(p.price),
            'quantity': p.quantity,
            'last_updated': p.last_updated
        } for p in products]
        return Response(data)

    def post(self, request):
        try:
            product = ProductService.create_product(
                name=request.data['name'],
                sku=request.data['sku'],
                price=float(request.data['price']),
                quantity=int(request.data['quantity'])
            )
            return Response({'message': 'Product created', 'sku': product.sku}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    """GET: retrieve, PUT: update, DELETE: delete a product by SKU."""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, sku: str) -> Product:
        try:
            return Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            raise ValueError(f"Product with SKU '{sku}' not found.")

    def get(self, request, sku: str):
        try:
            p = self.get_object(sku)
            data = {
                'name': p.name,
                'sku': p.sku,
                'price': float(p.price),
                'quantity': p.quantity,
                'last_updated': p.last_updated
            }
            return Response(data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, sku: str):
        try:
            product = ProductService.update_product(
                sku=sku,
                **{k: (float(v) if k == 'price' else int(v) if k == 'quantity' else v)
                   for k, v in request.data.items()}
            )
            return Response({'message': 'Product updated', 'sku': product.sku})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, sku: str):
        try:
            ProductService.delete_product(sku)
            return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
