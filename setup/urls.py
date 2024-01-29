from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API Rest",
        terms_of_service="#",
        contact=openapi.Contact(email="fehenriq.dev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("", include("apps.departments.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
