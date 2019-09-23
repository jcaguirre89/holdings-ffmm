from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView
from rest_framework import routers
from rest_framework.authtoken import views
from users.views import UserViewSet
from holdings.views import HoldingViewSet
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, "user")
router.register(r"holdings", HoldingViewSet, "holding")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-token-auth/", views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "openapi/",
        get_schema_view(title="Backend", description="Backend API"),
        name="openapi-schema",
    ),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="redoc",
    ),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
]
