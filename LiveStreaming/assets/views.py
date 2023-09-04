from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Venue, Team, Competition, Player, Match, TeamManager
from .serializers import *
import random, string

# Create your views here.
class ListOfVenues(generics.ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

class ListOfTeams(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class ListOfCompetition(generics.ListAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

class ListOfPlayers(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class ListOfMatches(generics.ListAPIView):
    queryset = Match.objects.filter(is_completed = False);
    serializer_class = MatchSerializer


class CreateVenueAPIView(APIView):
    '''
        when u use uploadData or FormData in your frontend/react instead of normal
        way of json.stringify, it send data in mutable way, it means the dictionary 
        it send to our backend is immutable not changable.. so when you use something 
        like .pop() here to capture data (pop remove the element of dictionary and return
        its value) it will bring an error of AttributeError: This "QueryDict instance is immutable"
        because data supplied by FormData is immutable so instead of using .pop() which tries 
        to change dict, just use .get() method which is read only..
    '''
    def post(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            address = request.data.get('address')

            new_venue = Venue.objects.create(
                name = name,
                address = address
            )

            new_venue.save()
            # since we need the id of the venue added we should send this in the response
            # for us maybe to utilize it to create team and other stuffs
            return Response({'status': 'Venue added successful', 'venue_id': new_venue.id})
        except Exception as err:
            return Response({"error": str(err)})

class FetchPlayersTeam(APIView):
    def post(self, request, *args, **kwargs):
        try:
            team_id = request.data.get('teamId')
            team = Team.objects.get(id=team_id)
            players = team.player_set.all()
            serializer = PlayerSerializer(players, many=True)
            return Response(serializer.data)
        
        except:
            return Response({"Error", "Something went wrong"})
           
           

class CreatePlayerAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            fname=request.data.get("fname")
            lname=request.data.get('lname')
            number=request.data.get('number')
            photo=request.data.get('profile', None)
            team_id=request.data.get('team')
            starter=request.data.get('starter')
            pType=request.data.get('ptype')
            pName=request.data.get('pname')

            starter = starter == "true" # this make sure starter is saved in 'boolean' and not string...
         
            team = Team.objects.get(id=team_id)
            if photo:
                new_player = Player.objects.create(
                    first_name=fname,
                    last_name=lname,
                    number=number,
                    photo=photo,
                    team=team,
                    starter=starter,
                    position_type=pType,
                    position_name=pName
                )
                new_player.save()
                return Response({"message":'New player have been created succesful'})
            
            new_player = Player.objects.create(
                first_name=fname,
                last_name = lname,
                number = number,
                team=team,
                starter=starter,
                position_type=pType,
                position_name=pName
            )
            new_player.save()
            return Response({"message": "New player have been created successful"})
            
            
        except Exception as err:
            return Response({"error": str(err)})

class CreateTeamAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            short = request.data.get('short')
            logo = request.data.get('logo')
            stadium = request.data.get('venue')
            competition_id = request.data.get('comp')
            managerLName = request.data.get('mlname')
            managerFName = request.data.get('mfname')
            managerPhoto = request.data.get('mphoto')

            
            # I EXPECT ALL REQUEST TO GIVE ME 'STADIUM' AND COMPETITION, NO OTHER OPTION...
            
            venue = Venue.objects.get(id=stadium)
            # also I should maybe save the team a user need to create here and then from that team instance
            # i should update a field of the 'stadium'
            new_team = Team.objects.create(
                name=name,
                short_name=short,
                logo=logo,
                stadium=venue
            )

            new_manager = TeamManager.objects.create(
                first_name = managerFName,
                last_name = managerLName,
                photo = managerPhoto,
                team = new_team
            )

            new_manager.save()

            new_team.save()
            competition = Competition.objects.get(id=competition_id)
            competition.teams.add(new_team)
            competition.save()
            return Response({'message': 'Team have been created succesful and the stadium/venue have been added to it', 'team_id': new_team.id})

        

        except Exception as err:
            return Response({"error": str(err)})


class GetTeamCoachAPIView(APIView):
    def post(self, request):
        try:
            team_id = request.data.get('team')

            team = Team.objects.get(id=team_id)
            # i've use dir() to check all attrbute belong to team.. and i think for reverse we need to have '_set' only for manytomany and 'onetomany' but for 'onetoone' relation no need
            manager = team.teammanager.id
            return Response({"manager": manager})
        except Exception as err:
            return Response({'error': 'Something went wrong..'})
    

class CreateMatchAPIView(APIView):
    def post(self, request): 
        try:
            comp = request.data.get('competition')
            hTeam = request.data.get('hteam')
            aTeam = request.data.get('ateam')
            stadium = request.data.get('venue')
            match = request.data.get('mname')
            eTime = request.data.get('etime')
            # isComplete = request.data.get('iscomplete')
            eTime = eTime == 'true'
            # isComplete = isComplete == 'true'
            global matchId
            matchId = ''
            existed_ids = Match.objects.values_list('matchId', flat=True)
            flag = True
            while flag:
                computed_matchId = "".join(random.choices(string.ascii_letters + string.digits, k=20))
                if computed_matchId not in existed_ids:
                    matchId = computed_matchId
                    flag=False
            
            competition = Competition.objects.get(id=int(comp))
            homeTeam = Team.objects.get(id=int(hTeam))
            awayTeam = Team.objects.get(id=int(aTeam))
            venue = Venue.objects.get(id=int(stadium))
            
            
            new_match = Match.objects.create(
                competition=competition,
                home_team = homeTeam,
                away_team = awayTeam,
                venue = venue,
                matchId = matchId,
                match_name = match,
                extraTime = eTime,
                # is_completed = isComplete
            )

            new_match.save()
            return Response({'message': 'Match have been created successful ', "match": new_match.matchId})
        except Exception as err: 
            return Response({"error": str(err)})
        



class CreateCompetitionAPIView(APIView):
    def post(self, request, *args, **kwargs):        
        try:
            # what we expect to receive from the frontend in order to create a competition
            name = request.data.get('name')
            logo = request.data.get('logo')
            # since we expect the user to 'add' teams in this case since it have the relation with
            # the team model, we expect here to 'receive' a list of 'ids' of teams added by the user 
            # in the competition.. But its not 'mandatory' the user can add the team later so here lets use 
            # the .get..
            print('THIS IS LOGO I RECEIVED FROM FRONTEND ', logo)

            teams = request.data.get('teams', None)
            
            if teams:
                ''' if user have been passed the ids of the teams to add we should get their teams
                instances and add them to the team field of the competition model...'''
                competition = Competition.objects.create(
                    name=name,
                    logo=logo
                )
                for team in teams:
                    team = Team.objects.get(id=team)
                    competition.add(team)
                competition.save()
                return Response({"message": 'Competition added successful with teams instances', "id": competition.id})
            else:
                competition = Competition.objects.create(
                    name=name,
                    logo=logo
                )
                competition.save()
                return Response({"message": 'Competition added successful no team instances added', "id": competition.id})
        except Exception as err:
            return Response({"error" : str(err)})

get_manager = GetTeamCoachAPIView.as_view()
create_match = CreateMatchAPIView.as_view()
team_players = FetchPlayersTeam.as_view()
fetch_venues = ListOfVenues.as_view()
fetch_matches = ListOfMatches.as_view()
fetch_teams = ListOfTeams.as_view()
fetch_players = ListOfPlayers.as_view()
fetch_competition = ListOfCompetition.as_view()
create_competition = CreateCompetitionAPIView.as_view()
create_team = CreateTeamAPIView.as_view()
create_venue = CreateVenueAPIView.as_view()
create_player = CreatePlayerAPIView.as_view()