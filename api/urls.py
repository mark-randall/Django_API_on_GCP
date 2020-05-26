from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from api import views

router = routers.DefaultRouter(trailing_slash=False)

router.register(
    prefix='feed', 
    viewset=views.FeedItemViewSet, 
    basename='feed'
)

router.register(
    prefix='feed/(?P<feed_id>[^/.]+)/comments',
    viewset=views.FeedItemCommentViewSet,
    basename='feed_comments'
)

router.register(
    prefix='feed/(?P<feed_id>[^/.]+)/images',
    viewset=views.ImageViewSet,
    basename='feed_images'
)

router.register(
    prefix='images', 
    viewset=views.ImageViewSet, 
    basename='image'
)

schema_view = get_swagger_view(title='Django API')

urlpatterns = router.urls + [url('docs', schema_view)]