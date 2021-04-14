from django.shortcuts import render

# Create your views here.
def home(response):
    args = {}
    return render(response, "IW/home.html", args)


def confirm(response):
    args = {}
    return render(response, "IW/confirmEmail.html", args)


def create(response):
    args = {}
    return render(response, "IW/create.html", args)


def tournaments(response):
    args = {}
    return render(response, "IW/tournaments.html", args)


def tournament(response, id):
    args = {
        "id": id
    }
    return render(response, "IW/tournament.html", args)