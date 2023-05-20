from django.urls import path
from rest_framework import routers
from products import views

router = routers.SimpleRouter()
router.register("device",views.DeviceView)
router.register("brand",views.BrandView)
router.register("category",views.CategoryView)
router.register('serial',views.SerialView)

app_name='products'
urlpatterns = [
    
]
urlpatterns+=router.urls
