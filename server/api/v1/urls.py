from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from server.api.v1.departments.views import DepartmentViewSet

app_name = 'v1'

router_v1 = DefaultRouter()

router_v1.register('departments', DepartmentViewSet, basename='departments')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
