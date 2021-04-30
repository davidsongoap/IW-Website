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
    args = {
        "range": range(12)
    }
    return render(response, "IW/tournaments.html", args)


def tournament(response, id):
    args = {
        "t_name": id
    }
    return render(response, "IW/tournament.html", args)
