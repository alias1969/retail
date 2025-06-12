from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

from config import settings

from partners.apps import PartnersConfig
from partners.views import CustomerViewSet, ContactViewSet

app_name = PartnersConfig.name

router = DefaultRouter()
router.register(r"customer", CustomerViewSet, basename="customer")
router.register(r"contacts", ContactViewSet, basename="contacts")

urlpatterns = []

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
