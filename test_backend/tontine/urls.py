from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register(r'package', views.PackageViewSet)
router.register(r'subscription', views.SubscriptionViewSet, "users-subscriptions")

urlpatterns = [
    url(r'^', include(router.urls))
]
