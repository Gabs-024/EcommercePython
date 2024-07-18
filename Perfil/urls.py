from django.urls import path
from .views import *

app_name="perfil"

urlpatterns = [
    path('criar', Criar.as_view(), name="criar"),
    path('atualizar/', Atualizar.as_view(), name="atualizar"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
 
]
