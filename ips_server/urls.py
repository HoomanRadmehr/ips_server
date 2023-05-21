from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from ips_server import settings

# schema_view = get_schema_view(
#    openapi.Info(
#       title="IPS server API",
#       default_version='v1',
#       description="Test description",
#     #   terms_of_service="https://www.google.com/policies/terms/",
#     #   contact=openapi.Contact(email="contact@snippets.local"),
#     #   license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )



urlpatterns = [
    path('admin/', admin.site.urls),
    path('rules/',include("rules.urls",namespace='rules')),
    path('users/',include("user_manager.urls",namespace="users")),
    path('products/',include("products.urls",namespace='products')),
   path('docs/', SpectacularAPIView.as_view(), name='schema'),
   path('docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
