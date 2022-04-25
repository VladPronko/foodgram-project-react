from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router = DefaultRouter()

# router.register(r'users/subscriptions', SubscriptionViewSet, basename='recipes')
router.register('users', CustomUserViewSet)


urlpatterns = [
    path(r'', include(router.urls)),
    # re_path(r'^api/', include('djoser.urls')),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]