from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, 'titles')
router.register('genres', GenreViewSet, 'genres')
router.register('categories', CategoryViewSet, 'categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    'reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    'comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
