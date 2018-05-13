from django import forms
from django.core.exceptions import ValidationError
from django.views import View

from Ekstraklasa.models import Players, RealTeam, Activities
from Ekstraklasa.validators import validate_username, validate_real_team


class LoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło użytkownika', widget=forms.PasswordInput)

class NewUserForm(forms.Form):
    username = forms.CharField(max_length=64, validators=[validate_username])
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    repassword = forms.CharField(max_length=64, widget=forms.PasswordInput)
    email = forms.EmailField()


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password2 = cleaned_data['repassword']
        if password != password2:
            raise ValidationError('Hasła nie są takie same!')

        return cleaned_data

class AddRealTeamForm(forms.Form):
    name = forms.CharField(max_length=64, label='Nazwa zespołu', validators=[validate_real_team])
    team_players = forms.FileField(label='Wgraj zawodników')

class UpdatePlayerForm(forms.ModelForm):
    class Meta:
        model = Players
        exclude = ['activities']

class AddFootballMatchPart1Form(forms.Form):
    date = forms.DateField(label='Termin', widget=forms.SelectDateWidget)
    time = forms.TimeField(label='Godzina', widget=forms.TimeInput)
    home_team_name = forms.ModelChoiceField(queryset=RealTeam.objects.all(), label='Drużyna gospodarzy')
    away_team_name = forms.ModelChoiceField(queryset=RealTeam.objects.all(), label='Drużyna gości')
    home_team_goals = forms.IntegerField(label='Gole gospodarzy')
    away_team_goals = forms.IntegerField(label='Gole gości')
    # home_yellow = forms.IntegerField(label='Ilość żółtych kartek gospodarzy')
    # home_red = forms.IntegerField(label='Ilość czerwonych kartek gospodarzy')
    # home_assists = forms.IntegerField(label='Ilość asyst gospodarzy')
    # away_assists = forms.IntegerField(label='Ilość asyst gości')
    # away_yellow = forms.IntegerField(label='Ilość żółtych kartek gości')
    # away_red = forms.IntegerField(label='Ilość czerwonych kartek gości')
    # home_substitutes = forms.IntegerField(label='Ilość zmian gospodarzy')
    # away_substitutes = forms.IntegerField(label='Ilość zmian gości')

    def clean(self):
        cleaned_data = super().clean()
        home_team = cleaned_data['home_team_name']
        away_team = cleaned_data['away_team_name']
        # home_substitutes = cleaned_data['home_substitutes']
        # away_substitutes = cleaned_data['away_substitutes']
        if home_team == away_team:
            raise ValidationError('Drużyna nie może grać sama ze sobą!')
        # if home_substitutes > 3 or away_substitutes > 3:
        #     raise ValidationError('Drużyna może przeprowadzić maksymalnie 3 zmiany!')


class AddFootballMatchPart2Form(forms.Form):
    home_team_players = forms.ModelMultipleChoiceField(label='Piłkarze drużyny gospodarzy',
                                                       queryset=Players.objects.none(),
                                                       widget=forms.CheckboxSelectMultiple)

    away_team_players = forms.ModelMultipleChoiceField(label='Piłkarze drużyny gości',
                                                       queryset=Players.objects.none(),
                                                       widget=forms.CheckboxSelectMultiple)

    def clean(self):
        cleaned_data = super().clean()
        try:
            home_team_players = cleaned_data['home_team_players']
            away_team_players = cleaned_data['away_team_players']
        except KeyError:
            raise ValidationError('Nie wybrano zawodników!')
        if home_team_players.count() > 14 or away_team_players.count() > 14:
            raise ValidationError('Wybrano za dużą ilość zawodników w jednej z drużyń!')
        if home_team_players.count() < 11 or away_team_players.count() < 11:
            raise ValidationError('Wybrano za małą ilość zawodników w jednej z drużyń!')


class AddFootballMatchPart3Form(forms.Form):
    player = forms.ModelChoiceField(label='Piłkarz',
                                    queryset=Players.objects.all())




