from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from partidas.views import dashboard, nova_partida, alterar_status, registrar_evento

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('times/', include('times.urls')),
    path('partidas/nova/', nova_partida, name='nova-partida'),
    path('partidas/<int:partida_id>/status/', alterar_status, name='alterar-status'),
    path('partidas/<int:partida_id>/evento/', registrar_evento, name='registrar-evento'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)