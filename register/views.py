from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})


def confirm(response):
    msg = ""
    user = response.user

    if response.method == "POST":
        form = ConfirmEmail(response.POST)
        if form.is_valid():

            code = form.data.get("confirmation_code")
            if user.confirmationcode.code == code:
                cc_table = user.confirmationcode
                cc_table.validated = True
                cc_table.save()
                return redirect("/tournaments")
            else:
                msg = "The code is incorrect"

    form = ConfirmEmail()


    if not response.user.is_authenticated:
        # redirects if user didn't login
        return redirect("/login")

    if user.is_superuser or user.is_staff or user.confirmationcode.validated:
        return redirect("/tournaments")
        # return render(response, "/tournaments.html", {})

    args = {
        "form": form,
        "message": msg
    }
    return render(response, "register/confirmEmail.html", args)


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
