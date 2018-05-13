"""Fantasy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from Ekstraklasa.views import LoginView, LogoutView, MainPageView, NewUserView, ConfirmationView, AddRealTeamView, \
    AllRealTeamsView, TeamPlayersView, DeleteTeamView, UpdateTeamNameView, UpdatePlayerView, DeletePlayerView, \
    CreateUserTeamView, UserTeamInfoView, CreateActivityView, AddMatchPart1View, AddMatchPart2View, AddMatchPart3View

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', MainPageView.as_view(), name='main'),
    url(r'^new_user/$', NewUserView.as_view(), name='new_user'),
    url(r'^confirmation/(?P<pk>(\d)+)/$', ConfirmationView.as_view(), name='confirmation'),
    url(r'^new_real_team/$', AddRealTeamView.as_view(), name='add_real_team'),
    url(r'^all_teams/$', AllRealTeamsView.as_view(), name='all_real_teams'),
    url(r'^real_team/(?P<pk>(\d)+)/$', TeamPlayersView.as_view(), name='real_team_players'),
    url(r'^delete_team/(?P<pk>(\d)+)/$', DeleteTeamView.as_view(), name='delete_team'),
    url(r'^update_team/(?P<pk>(\d)+)/$', UpdateTeamNameView.as_view(), name='update_team'),
    url(r'^update_player/(?P<pk>(\d)+)/$', UpdatePlayerView.as_view(), name='update_player'),
    url(r'^delete_player/(?P<pk>(\d)+)/$', DeletePlayerView.as_view(), name='delete_player'),
    url(r'^create_user_team/(?P<pk>(\d)+)/$', CreateUserTeamView.as_view(), name='create_user_team'),
    url(r'^user_team_info/(?P<pk>(\d)+)/$', UserTeamInfoView.as_view(), name='user_team_info'),
    url(r'^create_activity/$', CreateActivityView.as_view(), name='create_activity'),
    url(r'^add_match/1/$', AddMatchPart1View.as_view(), name='add_match_1'),
    url(r'^add_match/2/(?P<match_pk>(\d)+)/(?P<home_pk>(\d)+)/(?P<away_pk>(\d)+)/$', AddMatchPart2View.as_view(),name='add_match_2'),
    url(r'^add_match/3/(?P<match_pk>(\d)+)/(?P<home_pk>(\d)+)/(?P<away_pk>(\d)+)/$', AddMatchPart3View.as_view(), name='add_match_3')

]
