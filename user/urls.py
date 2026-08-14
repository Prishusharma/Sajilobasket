from django.urls import path
from .views import LogoutView, RegisterView, VendorTestView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
     path("login/",TokenObtainPairView.as_view(),name="login"),
     path("logout/",LogoutView.as_view(),name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("vendor-test/",VendorTestView.as_view(),name="vendor-test"),
]