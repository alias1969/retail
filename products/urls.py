from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

from config import settings

from products.apps import ProductsConfig
from products.views import ProductViewSet

app_name = ProductsConfig.name

router = DefaultRouter()
router.register("", ProductViewSet, basename="products")

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
