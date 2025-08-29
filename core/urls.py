from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.sistema, name='sistema'),
    path('login/', views.login, name="login"),
    path('registro/', views.registro, name="registro"),
    path('redefinir_senha/', views.redefinir_senha, name="redefinir-senha"),
]

