from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UsersViewSet, basename='users')

urlpatterns = [
    path(
        'v1/auth/token/',
        views.get_jwt_token,
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh/',
        views.get_jwt_token,
        name='token_refresh'
    ),
    path(
        'v1/auth/email/',
        views.send_confirmation_code,
        name='send_confirmation_code'
    ),
    path('v1/', include(router.urls))
]
