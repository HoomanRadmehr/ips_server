from django.urls import path
from rules import views


app_name = 'rules'
urlpatterns = [
    path("list",views.ListRuleView.as_view(),name="list"),
    path("retrieve/<str:pk>/",views.RetrieveRuleView.as_view(),name="retrieve"),
    path("verify/<str:rule_id>/",views.VerifiedRuleView.as_view(),name="verify_rule"),
    path('update/<str:pk>/',views.UpdateRuleView.as_view(),name="update"),
    path("",views.CreateRuleView.as_view(),name="create"),
]
