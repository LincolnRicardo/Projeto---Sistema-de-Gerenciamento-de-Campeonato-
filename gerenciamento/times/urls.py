from django.urls import path
from . import views

urlpatterns = [
    path('', views.TimeListView.as_view(), name='times-lista'),
    path('<int:pk>/', views.TimeDetailView.as_view(), name='time-detalhe'),
]