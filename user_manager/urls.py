from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenBlacklistView)
from user_manager import views


app_name='users'
urlpatterns = [
    path("email_verification",views.EmailVerificationView.as_view(),name="email_verification"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/",TokenBlacklistView.as_view(),name="logout"),
    path("create/",views.CreateUserView.as_view(),name="create"),
    path("retrieve/<str:user_id>/",views.RetrieveUserView.as_view(),name="retrive_user"),
    path("delete/<str:user_id>/",views.DeleteUserView.as_view(),name="delete_user"),
    path("update/<str:user_id>/",views.UpdateUserView.as_view(),name="update_user"),
    path("list",views.ListUsersView.as_view(),name="list"),
]
