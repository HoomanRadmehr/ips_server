from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from ips_server import settings


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
