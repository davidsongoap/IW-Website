from django.shortcuts import render, redirect
from .forms import *
from IW.models import *
import random
import string
from django.contrib.auth.decorators import login_required, user_passes_test
from PIL import Image
from IselWinner.settings import MEDIA_URL


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


@login_required(login_url="/login")
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


def check_admin(user):
    return user.is_superuser


@login_required(login_url="/login")
@user_passes_test(check_admin, login_url="/")
def create_tournament(response):
    if response.method == "POST":
        form = CreateTournament(response.POST, response.FILES)

        print(form.errors)
        print(response.FILES)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            name = data["tournament_name"]
            game_id = data["game"][:-1]
            visibility = data["visibility"]
            max_players = -1 if data["max_players"] == "unlimited" else int(data["max_players"])
            start_date = data["start_date"]
            cover_art = response.FILES.get("cover_art")
            desc = data["description"]
            password = data["password"] if visibility == "PRV" else None
            code = generate_code()

            t = Tournament(code, name=name, password=password, max_players=max_players,
                           start_date=start_date, cover_art=cover_art, visibility=visibility, admin_id=response.user,
                           description=desc)
            t.save()
            game = Game.objects.get(id=game_id)
            g_t = Tournament_Game(game_id=game, tournament_id=t)
            g_t.save()
            print("Torneio " + name + " criado")
            if cover_art != None:
                rescale_image(t.cover_art.path)
            return redirect("tournaments")
    else:
        form = CreateTournament()

    args = {
        "form": form,
    }

    return render(response, "register/createTournament.html", args)


@login_required(login_url="/login")
@user_passes_test(check_admin, login_url="/")
def upload_game(response):
    if response.method == "POST":
        print("GOT FORM")

        form = UploadGame(response.POST, response.FILES)
        if form.is_valid():
            data = form.cleaned_data
            name = data["game_name"]
            file = data["game_file"]
            author = data["author"]
            n_players = data["game_play"]
            game = Game(name=name, file=file, author=author, n_players=n_players)
            game.save()
            print()
        return redirect("tournaments")
    else:
        form = UploadGame()

    return render(response, "register/uploadGame.html", {"form": form})


def generate_code(size=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))


def rescale_image(image_path):
    im = Image.open(image_path)
    width, height = im.size
    if width != height:
        im_new = crop_max_square(im)
        im_new.save(image_path, quality=100)


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))
