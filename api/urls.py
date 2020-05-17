from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from .views import FeedItemViewSet
from .views import ImageViewSet
from .views import FeedItemCommentViewSet
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter(trailing_slash=False)

router.register('feed', FeedItemViewSet, basename='feed')

router.register(
    prefix='feed/(?P<feed_id>[^/.]+)/comments',
    viewset=FeedItemCommentViewSet,
    basename='feed_comments'
)

router.register(
    prefix='feed/(?P<feed_id>[^/.]+)/images',
    viewset=ImageViewSet,
    basename='feed_images'
)

## Use POST/PATCH feed/<feed_id> with 'existing_image_ids' param to associate an image with a feed iteem
router.register('images', ImageViewSet, basename='image')

schema_view = get_swagger_view(title='Django API')

urlpatterns = router.urls + [url('docs', schema_view)]