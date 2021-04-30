from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/confirmEmail")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})


def confirm(response):
    if response.method == "POST":
        form = ConfirmEmail(response.POST)
        if form.is_valid():
            pass  # ??
        return redirect("IW/tournaments")
    else:
        form = ConfirmEmail()

    return render(response, "register/confirmEmail.html", {"form": form})


def create_tournament(response):
    if response.method == "POST":
        form = CreateTournament(response.POST)
        if form.is_valid():
            pass  # ??
        return redirect("IW/tournaments")
    else:
        form = CreateTournament()

    return render(response, "register/createTournament.html", {"form": form})


def upload_game(response):
    if response.method == "POST":
        form = UploadGame(response.POST)
        if form.is_valid():
            pass  # ??
        return redirect("tournaments")
    else:
        form = UploadGame()

    return render(response, "register/uploadGame.html", {"form": form})
