from django.urls import path
from . import views
from register.forms import Login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),  # home page
    path("confirmEmail/", views.confirm, name="confirm"),  # pagina de confirmaçao de email
    path("createTournament/", views.create, name="create"),  # pagina para criar torneios
    path("tournaments/", views.tournaments, name="tournaments"),  # pagina com todos os torneios
    path("tournament/<str:id>/", views.tournament, name="tournament"),  # pagina de cada torneio (visto pelo id)
    path("redirectTournament", views.tournament_redirect, name="tournament"),  # pagina de cada torneio (visto pelo id)
    path("login/", auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=Login),
         name='login'),
]
