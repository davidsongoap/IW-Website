from django.shortcuts import render, redirect
from .models import *
from django.core.exceptions import *
import math
import random


# Create your views here.
def home(response):
    args = {}
    return render(response, "IW/home.html", args, )


def confirm(response):
    args = {}
    return render(response, "IW/confirmEmail.html", args)


def create(response):
    args = {}
    return render(response, "IW/create.html", args)


def tournaments(response):
    ts = Tournament.objects.all()
    args = {
        "ts": ts
    }
    return render(response, "IW/tournaments.html", args)


def tournament(response, code):
    if response.method == "POST":
        handle_tournament_page_post(response, code)
        return redirect("/tournament/" + code)
    user = response.user

    args = {}
    args["error"] = False

    try:
        t = Tournament.objects.get(code=code)
    except ObjectDoesNotExist:
        args["error"] = True
        args["error_message"] = "Tournament not found"
        return render(response, "IW/tournament.html", args)

    t = Tournament.objects.get(code=code)

    args["state"] = t.state
    # number of players participating
    player_count = t.participation_set.all().count()

    owner = User.objects.get(id=t.admin_id.id)

    is_owner = user.id == t.admin_id
    game = t.tournament_game_set.all()[0].game_id
    participants = t.participation_set.all()

    # all tournament matches
    all_match_list = []
    for match in t.match_set.all():
        match_list = []
        print(match.user_match_set.all().count())

        if match.user_match_set.all().count() == 0:
            # match that doesn't have players yet
            # put a placeholder
            match_list.append(["", ""])
            match_list.append(["", ""])

        else:
            # add the information of each participant on the match
            if match.user_match_set.all().count() == 1:
                match_list.append(["", ""])
            for participant in match.user_match_set.all():
                player_name = User.objects.get(id=participant.user_id_id).username
                score = participant.score if participant.score != None else ""
                match_list.append([player_name, score])

        # add this match to the list according to its number
        all_match_list.insert(match.num, match_list)

    max_players = t.max_players

    if max_players == -1:
        max_players = "∞"

    if game.n_players == 'S':
        t_type = 'SOLO'
        # needed to be inside another list
        temp = []
        temp.append(all_match_list)
        all_match_list = temp

    elif game.n_players == 'D':
        t_type = 'DUEL'
        all_match_list = reorganize_matches(all_match_list, player_count, 2)

    already_enrolled = t.participation_set.filter(user_id=user.id).exists()

    print(all_match_list)

    args["t"] = t
    args["t_type"] = t_type
    args["max_players"] = max_players
    args["player_count"] = player_count
    args["already_enrolled"] = already_enrolled
    args["is_owner"] = is_owner
    args["owner"] = owner
    args["if_full"] = is_tournament_full(t)
    args["game"] = game
    args["winner"] = t.winner_id
    args["matches"] = all_match_list

    return render(response, "IW/tournament.html", args)


################### Utility Functions ########################

def reorganize_matches(match_list, n_players, players_per_match):
    new_list = []
    i = 0
    temp = []
    n_players = n_players / players_per_match
    for match in match_list:
        if i == n_players:
            n_players /= players_per_match
            new_list.append(temp)
            temp = []
            i = 0
        i += 1
        temp.append(match)
        if n_players == 1: new_list.append(temp)
    return new_list


def tournament_redirect(response):
    t_code = response.GET.get('t_code')
    return redirect("/tournament/" + t_code)


def start_tournament(t):
    print("starting tournament..")
    participants = list(t.participation_set.all())
    game = t.tournament_game_set.all()[0].game_id
    n_players = game.n_players
    n_matches = len(participants) - 1

    if n_players == 'D':  # duels
        generate_duel(t, participants, n_matches)

    elif n_players == 'S':
        m = Match(num=0, tournament_id=t)
        m.save()
        for p in participants:
            m_p = User_Match(user_id=p.user_id, match_id=m)
            m_p.save()


def generate_duel(t, participants, n_matches):
    random.shuffle(participants)

    # create all matches
    for j in range(n_matches):
        m = Match(num=j, tournament_id=t)
        m.save()

    # populate the first round of matches with the players
    i = 0
    while participants:
        p1 = participants.pop().user_id
        p2 = participants.pop().user_id
        m = Match.objects.get(tournament_id=t, num=i)
        m_p1 = User_Match(user_id=p1, match_id=m)
        m_p2 = User_Match(user_id=p2, match_id=m)
        m_p1.save()
        m_p2.save()
        i += 1


def handle_tournament_page_post(response, code):
    post = response.POST
    cur_state = post["current-state"]
    if cur_state == "Edit":
        pass
    elif cur_state == "Enroll":
        enroll(response, code)
    elif cur_state == "CancelEnroll":
        cancel_enroll(response, code)
    else:
        t = Tournament.objects.get(code=code)
        t.state = cur_state
        t.save()
        if cur_state == "ST":
            start_tournament(t)


def is_tournament_full(t):
    if t.state == 'ST' or t.state == "CL": return True
    if t.max_players == -1:
        is_full = False
    else:
        is_full =  t.participation_set.all().count() >= t.max_players

    return is_full


def enroll(response, code):
    t = Tournament.objects.get(code=code)
    if_full = is_tournament_full(t)

    if not if_full:
        Participation(tournament_id=t, user_id=response.user).save()


def cancel_enroll(response, code):
    t = Tournament.objects.get(code=code)
    if t.state == 'OP':
        p = Tournament.objects.get(code=code).participation_set.all()
        p.get(user_id=response.user).delete()
