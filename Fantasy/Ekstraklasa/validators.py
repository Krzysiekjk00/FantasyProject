from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from Ekstraklasa.models import RealTeam


def validate_username(value):
    if User.objects.filter(username=value):
        raise ValidationError('Użytkownik o nazwie {} już istnieje'.format(value))

def validate_real_team(value):
    if RealTeam.objects.filter(name=value):
        raise ValidationError('Zespół o nazwie {} już istnieje'.format(value))