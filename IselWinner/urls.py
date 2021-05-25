"""IselWinner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from IselWinner import settings
from register import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', v.register, name="register"),  # pagina de registo no website
    path("confirmEmail/", v.confirm, name="confirm"),  # pagina de confirmaçao de email
    path("createTournament/", v.create_tournament, name="create"),  # pagina para criar torneios
    path("uploadGame/", v.upload_game, name="upload"),  # pagina para dar upload a jogos
    path('', include("IW.urls")),
    path('', include("django.contrib.auth.urls")),

]
if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
