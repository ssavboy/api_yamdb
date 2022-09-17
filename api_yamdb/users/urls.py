from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_jwt_token, register

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', register),
    path('token/', get_jwt_token),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls)),
]
