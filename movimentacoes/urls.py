from django.urls import path
from movimentacoes import views

app_name = 'movimentacoes'

urlpatterns = [
    path('movimentacoes/', views.movimentacoes, name='movimentacoes'),
]
