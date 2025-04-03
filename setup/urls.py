from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenRefreshView

from utils.token import CustomTokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="Requisitions API",
        default_version="v1",
        description="API Rest",
        terms_of_service="#",
        contact=openapi.Contact(email="dev2@engenhadev.com"),
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
    path("", include("apps.products.urls")),
    path("", include("apps.purchases.urls")),
    path("", include("apps.services.urls")),
    path("", include("apps.providers.urls")),
    path("", include("apps.contracts.urls")),
    path("", include("apps.freights.urls")),
    path("", include("apps.maintenances.urls")),
    path("", include("apps.employees.urls")),
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token-obtain"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
