from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

VISIBILITY_CHOICES = (
    ('private', 'Private'),
    ('public', 'Public'),
)

MAX_PLAYERS_CHOICES = (
    ('unlimited', 'Unlimited'),
    ('2', '2'),
    ('4', '4'),
    ('8', '8'),
    ('16', '16'),
    ('32', '32'),
    ('64', '64'),
)

GAME_PLAY_CHOICES = (
    ('S', 'Solo'),
    ('D', '1 vs 1'),
)

GAME_NAME_CHOICES = (
    ('jogo1', '4 EM LINHA'),
    ('jogo2', 'XADREZ'),
    ('jogo3', 'DAMAS'),
)

START_DATE_CHOICES = (
    ('hoje', '15/04/2021'),
    ('amanha', '16/04/2021'),
    ('depois', '17/04/2021'),
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'placeholder': 'Email*'})
        self.fields['email'].label = False
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username*'})
        self.fields['username'].label = False
        self.fields['username'].help_text = None
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password*'})
        self.fields['password1'].label = False
        self.fields['password1'].help_text = None
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Repetir Password*'})
        self.fields['password2'].label = False
        self.fields['password2'].help_text = None


class Login(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username*'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password*'})
        self.fields['password'].label = False


class ConfirmEmail(forms.Form):
    confirmation_code = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['confirmation_code']

    def __init__(self, *args, **kwargs):
        super(ConfirmEmail, self).__init__(*args, **kwargs)
        self.fields['confirmation_code'].widget = forms.TextInput(attrs={'placeholder': 'Confirmation Code*'})
        self.fields['confirmation_code'].label = False


class CreateTournament(forms.Form):
    tournament_name = forms.CharField(max_length=25)
    game = forms.CharField(widget=forms.Select(choices=GAME_NAME_CHOICES))
    visibility = forms.CharField(widget=forms.Select(choices=VISIBILITY_CHOICES))
    password = forms.CharField(max_length=15)
    max_players = forms.CharField(widget=forms.Select(choices=MAX_PLAYERS_CHOICES))
    start_date = forms.DateTimeField()
    cover_art = forms.FileField(label='Select game file', widget=forms.FileInput(attrs={'accept': '.png,.jpg'}))
    description = forms.CharField(widget=forms.Textarea, max_length=50)

    class Meta:
        model = User
        fields = ['tournament_name', 'game', 'visibility', 'password', 'max_players', 'start_date', 'cover_art', 'description']

    def __init__(self, *args, **kwargs):
        super(CreateTournament, self).__init__(*args, **kwargs)
        self.fields['tournament_name'].widget = forms.TextInput(attrs={'placeholder': 'Tournament Name*'})
        self.fields['tournament_name'].label = False
        self.fields['password'].widget = forms.TextInput(attrs={'placeholder': 'Password'})
        self.fields['password'].label = False
        self.fields['description'].widget = forms.TextInput(attrs={'placeholder': 'Description*'})
        self.fields['description'].label = False
        self.fields['visibility'].label = False
        self.fields['max_players'].label = False
        self.fields['game'].label = False
        self.fields['start_date'].label = False
        self.fields['start_date'].widget = forms.TextInput(attrs={'placeholder': 'Choose time and day for the tournament to start*'})
        self.fields['cover_art'].label = False


class UploadGame(forms.Form):
    game_name = forms.CharField(max_length=25)
    game_file = forms.FileField(label='Select game file', widget=forms.FileInput(attrs={'accept': '.jar,.py,.exe,.zip'}))
    game_play = forms.CharField(widget=forms.Select(choices=GAME_PLAY_CHOICES))
    author = forms.CharField(max_length=25)

    class Meta:
        model = User
        fields = ['game_name', 'code_name', 'game_file', 'author']

    def __init__(self, *args, **kwargs):
        super(UploadGame, self).__init__(*args, **kwargs)
        self.fields['game_name'].widget = forms.TextInput(attrs={'placeholder': 'Game Name*'})
        self.fields['game_name'].label = False
        self.fields['game_file'].label = False
        self.fields['author'].widget = forms.TextInput(attrs={'placeholder': 'Author*'})
        self.fields['author'].label = False
        self.fields['game_play'].label = False
