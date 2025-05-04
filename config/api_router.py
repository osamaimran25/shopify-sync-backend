from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from django.urls import include
from django.urls import path

from synch_backend.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# router.register("users", UserViewSet)
urlpatterns = [
path('product/', include('apps.product.urls.product_urls_v1')),

]
app_name = "api"
