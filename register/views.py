from django.shortcuts import render


# Create your views here.
def register(response):
    return render(response, "register/register.html", {})