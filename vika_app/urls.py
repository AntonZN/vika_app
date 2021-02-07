from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from vika_app.main import views

from rest_framework.schemas import get_schema_view
from rest_framework import permissions

from drf_yasg.views import get_schema_view as get_schema_view_yasg
from drf_yasg import openapi


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("vika_app.main.api.v1.urls")),
    path("video-list/", views.video_list, name="video-list"),
    path("video-list/<video_uuid>/", views.video_rating),
]

schema_url_patterns = [
    path("api/v1/", include("vika_app.main.api.v1.urls")),
]


schema_view_yasg = get_schema_view_yasg(
    openapi.Info(
        title="VIKA API",
        default_version="v1",
        description="""The `swagger-ui` view can be found [here](/cached/swagger).
The `ReDoc` view can be found [here](/redoc).
The swagger YAML document can be found [here](/swagger.yaml).""",
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
    patterns=schema_url_patterns,
)

urlpatterns += [
    re_path(
        r"^swagger-rest(?P<format>\.json|\.yaml)$",
        schema_view_yasg.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger-rest/",
        schema_view_yasg.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view_yasg.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
