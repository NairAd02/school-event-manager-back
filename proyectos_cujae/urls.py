from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from app_ponencias.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Eventos API',
        default_version='v1',
    ),
    public=True,
)

urlpatterns = (
        [
            path('admin/', admin.site.urls),
            # path('upload/', upload_file, name='upload'),
            path('', eventos_view, name='eventos_view'),
            path('add/', eventos_add, name='eventos_add'),
            path('change/<int:evento_id>/', eventos_change, name='eventos_change'),

            path('ponencias/', ponencias_view, name='ponencias_view'),
            path('ponencias/add/', ponencias_add_1, name='ponencias_add_1'),
            path('ponencias/add/<int:ponencia_id>/', ponencias_add_2, name='ponencias_add_2'),
            # path('ponencias/change/<int:ponencia_id>/', ponencias_change, name='ponencias_change'),
            path('ponencias/ia/summary/<int:ponencia_id>/', ponencias_ia_summary, name='ponencias_ia_summary'),
            path('api/eventos/', EventoListCreateApi.as_view()),
            path('api/eventos/<int:pk>/', EventoRetrieveUpdateDestroyApi.as_view()),

            path('api/ponencias/', PonenciaListCreateApi.as_view()),
            path('api/ponencias/<int:pk>/', PonenciaRetrieveUpdateDestroyApi.as_view()),
            path('api/ponencias/evento/<int:evento_id>/', PonenciaByEvento.as_view()),
            re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
            path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
