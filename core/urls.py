from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from core.settings import *
from django.conf.urls.static import static
schema_view = get_schema_view(
    openapi.Info(
        title="Elimu Pay",
        default_version='v1',
        description="API documentation for Elimu Pay",
    ),
    public=True,
    permission_classes=[permissions.AllowAny]

)

urlpatterns = [
    path('api/v1/students/', include('students.urls')),
    path('api/v1/expenses/', include('expenses.urls')),
    path('api/v1/schools/', include('schools.urls')),
    path('api/v1/parents/', include('parents.urls')),
    path('api/v1/fee/', include('fee.urls')),
    # path('api/v1/feecollections/', include('feecollections.urls')),
    path("api/v1/suppliers/", include("suppliers.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/supportstaffs/", include("supportstaffs.urls")),
    path("api/v1/usergroup/", include("usergroup.urls")),
    path("api/v1/mpesa/", include("mpesa.urls")),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
