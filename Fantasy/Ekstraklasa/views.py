from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView, CreateView
from tablib import Dataset

from Ekstraklasa.forms import LoginForm, NewUserForm, AddRealTeamForm, UpdatePlayerForm, AddFootballMatchPart1Form, \
    AddFootballMatchPart2Form, AddFootballMatchPart3Form
from Ekstraklasa.models import RealTeam, Players, UserTeam, Activities, FootballMatch
from Ekstraklasa.resources import PlayerResource


class LoginView(View):

    def get(self, request):
        ctx = {
            'form': LoginForm()
        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                url = request.GET.get('next')
                if url:
                    return redirect(url)
                return HttpResponseRedirect(reverse('main'))
            else:
                form.add_error(field=None, error='Zły login lub hasło')
        ctx = {
            'form': LoginForm()
        }
        return render(request, 'login.html', ctx)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))

class NewUserView(View):
    def get(self, request):
        form = NewUserForm()
        ctx = {
            'form': form,
        }
        return render(request, 'newuser.html', ctx)

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            del form.cleaned_data['repassword']
            user = User.objects.create_user(**form.cleaned_data)
            return HttpResponseRedirect(reverse('confirmation', kwargs={'pk':user.id}))
        ctx = {
            'form': form,
        }
        return render(request, 'newuser.html', ctx)

class ConfirmationView(View):
    def get(self, request, pk):
        ctx = {
            'new_user': User.objects.get(pk=pk)
        }
        return render(request, 'confirmation.html', ctx)


class MainPageView(LoginRequiredMixin, View):

    def get(self, request):
        all_user_teams = UserTeam.objects.order_by('-team_points').all()
        for team in all_user_teams:
            points = 0
            for player in team.team_players.all():
                points += player.overall_points
            team.team_points = points
            team.save()
        ctx = {
            'user_teams': UserTeam.objects.order_by('-team_points').all()
        }
        return render(request, 'main.html', ctx)

class AddRealTeamView(View):

    def get(self, request):
        form = AddRealTeamForm()
        ctx = {
            'form': form,
        }
        return render(request, 'add_real_team.html', ctx)

    def post(self, request):
        form = AddRealTeamForm(request.POST, request.FILES)
        if form.is_valid():
            new_team = RealTeam.objects.create(name=form.cleaned_data['name'])

            player_resource = PlayerResource()
            dataset = Dataset()
            new_players = request.FILES['team_players']


            imported_data = dataset.load(new_players.read().decode('utf-8'), format='csv')
            result = player_resource.import_data(dataset, dry_run=True)

            if not result.has_errors():
                player_resource.import_data(dataset, dry_run=False)
                all_players = Players.objects.filter(team_id=None)
                for player in all_players:
                    player.team = new_team
                    player.save()
                return HttpResponseRedirect(reverse('main'))
            return HttpResponseRedirect(reverse('main'))
        ctx = {
            'form': form,
        }
        return render(request, 'add_real_team.html', ctx)

class AllRealTeamsView(View):

    def get(self, request):
        ctx = {
            'teams': RealTeam.objects.order_by('name').all()
        }
        return render(request, 'all_real_teams.html', ctx)

class TeamPlayersView(View):

    def get(self, request, pk):
        ctx = {
            'team': RealTeam.objects.get(pk=pk),
            'players': Players.objects.order_by('position').filter(team_id=pk),
        }
        return render(request, 'real_team_players.html', ctx)

class DeleteTeamView(DeleteView):
    model = RealTeam
    success_url = '/all_teams'

class UpdateTeamNameView(UpdateView):
    model = RealTeam
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('all_real_teams')

class UpdatePlayerView(View):

    def get(self, request, pk):
        updated_player = Players.objects.get(pk=pk)
        form = UpdatePlayerForm(instance=updated_player)
        ctx = {
            'form': form,
        }
        return render(request, 'update_player.html', ctx)

    def post(self, request, pk):
        updated_player = Players.objects.get(pk=pk)
        form = UpdatePlayerForm(request.POST, instance=updated_player)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('real_team_players', kwargs={'pk':updated_player.team_id}))
        ctx = {
            'form': form,
        }
        return render(request, 'update_player.html', ctx)

class DeletePlayerView(View):

    def get(self, request, pk):
        ctx = {
            'player': Players.objects.get(pk=pk)
        }
        return render(request, 'delete_player.html', ctx)

    def post(self, request, pk):
        deleted_player = Players.objects.get(pk=pk)
        deleted_player.delete()
        return HttpResponseRedirect(reverse('real_team_players', kwargs={'pk': deleted_player.team_id}))

class CreateUserTeamView(View):

    def get(self, request, pk):
        ctx = {
            'goalkeepers': Players.objects.order_by('overall_points').filter(position=1),
            'defenders': Players.objects.order_by('overall_points').filter(position=2),
            'midfielders': Players.objects.order_by('overall_points').filter(position=3),
            'strikers': Players.objects.order_by('overall_points').filter(position=4)
        }
        return render(request, 'create_user_team.html', ctx)

    def post(self, request, pk):
        all_players = []
        for i in range(1, 16):
            player_id = request.POST.get('player_{}'.format(i))
            player = Players.objects.get(pk=int(player_id))
            all_players.append(player)
        if len(all_players) != len(set(all_players)):
            raise Exception('Każdy zawodnik musi być inny!')
        if len(all_players) != 15:
            raise Exception('Musisz wybrać 15 zawodników!')
        user = User.objects.get(pk=pk)
        new_user_team = UserTeam.objects.create(name=request.POST.get('user_team_name'), user=user)
        new_user_team.team_players.set(all_players)
        new_user_team.save()
        return HttpResponseRedirect(reverse('main'))

class UserTeamInfoView(View):

    def get(self, request, pk):
        team = UserTeam.objects.get(pk=pk)
        ctx = {
            'team': team,
        }
        return render(request, 'user_team_info.html', ctx)

class CreateActivityView(CreateView):
    model = Activities
    fields = ['name', 'point_value']
    success_url = reverse_lazy('main')

class AddMatchPart1View(View):

    def get(self, request):
        form = AddFootballMatchPart1Form()
        ctx = {
            'form': form
        }
        return render(request, 'match_part_1.html', ctx)

    def post(self, request):
        form = AddFootballMatchPart1Form(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            home_team = RealTeam.objects.get(name=form.cleaned_data['home_team_name'])
            away_team = RealTeam.objects.get(name=form.cleaned_data['away_team_name'])
            home_goals = form.cleaned_data['home_team_goals']
            away_goals = form.cleaned_data['away_team_goals']
            new_match = FootballMatch.objects.create(date=date, time=time, home_team_goals=home_goals, away_team_goals=away_goals,
                                         home_team_name=home_team, away_team_name=away_team)
            return HttpResponseRedirect(reverse('add_match_2', kwargs={'match_pk': new_match.id,
                                                                       'home_pk': home_team.id,
                                                                       'away_pk': away_team.id}))
        else:
            ctx = {
                'form': form
            }
            return render(request, 'match_part_1.html', ctx)

class AddMatchPart2View(View):

    def get(self, request, match_pk, home_pk, away_pk):
        form = AddFootballMatchPart2Form()
        form.fields['home_team_players'].queryset = Players.objects.filter(team_id=home_pk)
        form.fields['away_team_players'].queryset = Players.objects.filter(team_id=away_pk)

        ctx = {
            'form': form,

        }
        return render(request, 'match_part_2.html', ctx)

    def post(self, request, match_pk, home_pk, away_pk):
        form = AddFootballMatchPart2Form(request.POST)
        form.fields['home_team_players'].queryset = Players.objects.filter(team_id=home_pk)
        form.fields['away_team_players'].queryset = Players.objects.filter(team_id=away_pk)

        if form.is_valid():
            home_team_players = form.cleaned_data['home_team_players']
            away_team_players = form.cleaned_data['away_team_players']
            match = FootballMatch.objects.get(pk=match_pk)
            match.home_team_players.set(home_team_players)
            match.away_team_players.set(away_team_players)
            match.save()
            return HttpResponseRedirect(reverse('add_match_3', kwargs={'match_pk': match_pk,
                                                                       'home_pk': home_pk,
                                                                       'away_pk': away_pk}))
        ctx = {
            'form': form,
        }
        return render(request, 'match_part_2.html', ctx)

class AddMatchPart3View(View):

    def get(self, request, match_pk, home_pk, away_pk):

        match = FootballMatch.objects.get(pk=match_pk)
        match_goals = match.home_team_goals + match.away_team_goals

        class Form(AddFootballMatchPart3Form):
            def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                         label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None,
                         renderer=None):
                super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted,
                                 field_order, use_required_attribute, renderer)
                self.fields['player'].queryset = Players.objects.filter(team_id__in=[home_pk, away_pk])

        playersFormSet = formset_factory(Form, min_num=match_goals, max_num=match_goals)()

        ctx = {
            'form': playersFormSet
        }
        return render(request, 'match_part_3.html', ctx)

    def post(self, request, match_pk, home_pk, away_pk):
        match = FootballMatch.objects.get(pk=match_pk)
        match_goals = match.home_team_goals + match.away_team_goals
        playersFormSet = formset_factory(AddFootballMatchPart3Form, min_num=match_goals, max_num=match_goals)(request.POST)
        if playersFormSet.is_valid():
            for player in playersFormSet:
                player_name = player.cleaned_data['player']
                activity = Activities.objects.get(name='Gol')
                player_object = Players.objects.get(name=player_name)
                player_object.overall_points = player_object.overall_points + 4
                player_object.save()
            return HttpResponseRedirect(reverse('main'))
        ctx = {
            'form': playersFormSet
        }
        return render(request, 'match_part_3.html', ctx)

























