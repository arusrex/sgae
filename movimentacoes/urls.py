from django.urls import path
from movimentacoes import views

app_name = 'movimentacoes'

urlpatterns = [
    path('matriculas/', views.matriculas, name='matriculas'),
    path('remanejamentos/', views.remanejamentos, name='remanejamentos'),
    path('transferencias/', views.transferencias, name='transferencias'),
]
