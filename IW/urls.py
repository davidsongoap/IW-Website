from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # home page
    path("confirmEmail/", views.confirm, name="confirm"),  # pagina de confirmaçao de email
    path("createTournament/", views.create, name="create"),  # pagina para criar torneios
    path("tournaments/", views.tournaments, name="tournaments"),  # pagina com todos os torneios
    path("tournament/<str:id>/", views.tournament, name="tournament"),  # pagina de cada torneio (visto pelo id)
]
