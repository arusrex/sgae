from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.usuarios, name='usuarios'),
    path('novo-usuario/', views.novo_usuario, name='novo-usuario'),
    path('editar-usuario/<str:pk>/', views.editar_usuario, name='editar-usuario'),
    path('excluir-usuario/<str:pk>/', views.excluir_usuario, name='excluir-usuario'),
]
