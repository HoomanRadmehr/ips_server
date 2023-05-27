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
    path('assign_rule/',views.AssignRuleView.as_view(),name="assign_rule"),
    path('assign_owner/',views.AssignOwnerView.as_view(),name="assign_owner"),
]
urlpatterns+=router.urls
