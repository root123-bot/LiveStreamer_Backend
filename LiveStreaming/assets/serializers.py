from rest_framework import serializers
from .models import *

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = [
            'id',
            'name',
            'logo',
            'teams'
        ]

class MatchSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Match
        fields = [
            'id', 
            'competition',
            'home_team',
            'away_team',
            'venue',
            'matchId',
            'extraTime',
            'addedAt',
            'hteamname',
            'hteamlogo',
            'ateamname',
            'ateamlogo',
            'stadium'
        ]

class PlayerSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Player
        fields = [
            'id',
            'first_name',
            'last_name',
            'photo',
            'team',
            'starter',
            'position_type',
            'position_name',
            'number',
            'team_logo'
        ]


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            'id',
            'name',
            'address'
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'short_name',
            'logo',
            'stadium',
            'get_venueId'
        ]