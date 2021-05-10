from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver


##### Models #####

class ConfirmationCode(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=15, unique=True)
    validated = models.BooleanField(default=False)

    def __str__(self):
        return 'ConfirmationCode (user={} | confirm_code={})'.format(str(self.user), self.code)


class ProfileImage(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pic/', null=True, blank=True)

    def __str__(self):
        return 'ProfileImage (user={} | image={})'.format(str(self.user), self.image)


class Tournament(models.Model):
    STARTED = 'ST'
    OPEN = 'OP'
    PLANNED = 'PL'
    CLOSED = 'CL'
    ENDED = 'EN'

    TStates = [
        (STARTED, 'Started'),
        (OPEN, 'Enrollments'),
        (PLANNED, 'Planned'),
        (CLOSED, 'Closed'),
        (ENDED, 'Finished')
    ]

    PRIVATE = 'PRV'
    PUBLIC = 'PUB'

    TVisibility = [
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
    ]

    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30, null=False)
    password = models.CharField(max_length=25, null=True)
    max_players = models.IntegerField(null=True, blank=True)
    start_date = models.DateField()
    winner_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="winner")
    full = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    cover_art = models.ImageField(upload_to='t_cover_arts/', null=True, blank=True)
    visibility = models.CharField(max_length=3, choices=TVisibility)
    state = models.CharField(max_length=2, choices=TStates, default=PLANNED)
    admin_id = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="admin")

    def __str__(self):
        return 'Tournament(code={} | name={} | admin_id={} | visibility={} | state={})'.format(self.code, self.name,
                                                                                               self.admin_id,
                                                                                               self.visibility,
                                                                                               self.state)


class Game(models.Model):
    SOLO = 'S'
    DUEL = 'D'

    NPlayers = [
        (SOLO, 'S'),
        (DUEL, 'D')
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    file = models.FileField(upload_to='game_files/')
    author = models.CharField(max_length=100)
    n_players = models.CharField(max_length=1, choices=NPlayers)

    def __str__(self):
        return 'Game (name={} | author={} | n_players={})'.format(self.name, self.author, self.n_players)


class Tournament_Game(models.Model):
    id = models.AutoField(primary_key=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return 'Tournament_Game (tournament_id={} | game_id={})'.format(self.tournament_id, self.game_id)


class Invitations(models.Model):
    id = models.AutoField(primary_key=True)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Invitation (tournament_id={} | user_id={})'.format(self.tournament_id, self.user_id)


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    num = models.IntegerField()
    tournament_id = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.IntegerField()

    def __str__(self):
        return 'Match (num={} | tournament_id={} | round={})'.format(self.num, self.tournament_id, self.round)


class User_Match(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)

    def __str__(self):
        return 'Match (user_id={} | match_id={} | score={})'.format(self.user_id, self.user_id, self.score)


class Moves(models.Model):
    id = models.AutoField(primary_key=True)
    move = models.TextField(max_length=300)


class Match_Moves(models.Model):
    id = models.AutoField(primary_key=True)
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    move_id = models.ForeignKey(Moves, on_delete=models.CASCADE)
