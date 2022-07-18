from django.urls import path, include, re_path
import polaris.urls
from rest_framework import routers

from django.contrib.auth import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
from .views import all_fields_form_view, confirm_email, skip_confirm_email

urlpatterns = [
    re_path(
        "login",
        views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("all-fields", all_fields_form_view),
    path("confirm_email", confirm_email, name="confirm_email"),
    path("skip_confirm_email", skip_confirm_email, name="skip_confirm_email"),
    path('', include(polaris.urls)),
]
