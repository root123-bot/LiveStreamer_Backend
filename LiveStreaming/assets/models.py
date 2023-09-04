from django.db import models
import time

POSITION_TYPE = (
    ('Goalkeeper', 'Goalkeeper'),
    ('Defender', 'Defender'),
    ('Midfielder', 'Midfielder'),
    ('Forward', 'Forward')
)

# here we only use initials... 
POSITION_NAME = (
    ('GK', 'GK'),
    ('CB', 'CB'),
    ('RB', 'RB'),
    ('LB', 'LB'),
    ('DM', 'DM'),
    ('LW', 'LW'),
    ('RW', 'RW'),
    ('AM', 'AM'),
    ('CM', 'CM'),
    ('DM', 'DM'),
    ('S', 'S'),
    ('FW', 'FW'),
    ('CF', 'CF')
)


class Venue(models.Model):
    name=models.CharField(max_length=400, unique=True)
    address=models.CharField(max_length=400)

    def __str__(self):
        return self.name    

class Team(models.Model):
    name=models.CharField(max_length=400, unique=True)
    '''
        is there is a need for the 'shortname' to be uniques.. ? The answer is YES 
        because on match we display the shortname so what happens when two teams meets
        together, it will be misserable??? Yes.. But if you made it unique what will 
        happen.. But for case you have 100 teams and all of them there is small chance of 
        meeting each other, for example lets say SIMBA (SSC) and Real Madrid these two 
        teams if they have the same shortname there is no chances of them meeting each other 
        for this i thought i will use "unique_together' but this will not work 
        if models fields are from different model.. unique_together used only inside the 
        same model.. SO AS I SAID FOR NOW LETS LEAVE THIS AS unique=True, for later i will
        think about it...
    '''
    short_name=models.CharField(max_length=4, unique=True)  # this is shortname of team we should limit only 4 characters long
    logo = models.ImageField(upload_to='images/')
    # venue = models.CharField(max_length=400)  # this is venue belong to the team we can need it or it can be overriden with new venue if both teams(away/home) does not play in their stadiums
    # one team one venue, oneVenue many teams... ukiweka hapa onetoone endapo mtu atakimiliki kiwanja fulani basi huwezi ukampa mtu mwingine hicho kiwanja.. so it act in all direction, ni sawa
    # tu na profile unakumbuka kuwa profile moja ilikua ina-associted with only one user/email so uki-iassign nyingine lazima itakataaa..
    stadium=models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def get_venueId(self):
        return self.stadium.id

    def __str__(self):
        return self.name

class TeamManager(models.Model):
    first_name = models.CharField(max_length=400)
    last_name = models.CharField(max_length=400)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    # one team one manager, one manager one team
    team = models.OneToOneField(Team, on_delete=models.CASCADE) 

    def __str__(self):
        return self.first_name + self.last_name
# Create your models here.
class Competition(models.Model):
    name=models.CharField(max_length=400, unique=True)
    logo = models.ImageField(upload_to='images/')
    teams = models.ManyToManyField(Team, blank=True)               # one compet vs one team, one team vs many competition.. we need to allow 'blank/null=true' bcoz we can create the competition and we can add teams later... 

    def __str__(self):
        return self.name

class Player(models.Model):
    first_name=models.CharField(max_length=400)
    last_name=models.CharField(max_length=400)
    number=models.PositiveIntegerField()
    photo=models.ImageField(upload_to='images/', blank=True, null=True)
    # one player to one team.... one team to many players..
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    starter = models.BooleanField(default=False)
    position_type = models.CharField(max_length=20, choices=POSITION_TYPE)  # Here its a major position of player.. all midfielder appear with 'Midfielder' name
    position_name = models.CharField(max_length=5, choices=POSITION_NAME)

    @property
    def team_logo(self):
        return self.team.logo.url

    def __str__(self):
        return self.first_name + ' ' + self.last_name
# the match should be stored in the database and database should count for the match continously untill the match is marked as 'completed' by the user justi like
# in the ligr.live here i see even if umeme umekatika in your match dashboard unaikuta match yake kama huku-icomplete then unaweza ukastart from there .. so so that 
# purpose we should have the model made for this purpose so as to attract more user.. WASIJE USER WAKASEMA MAYBE COZ UMEME ULIKATIKA KWANGU NILIVYOKUWA NA LIVE-STREAM BASI
# INABIDI NIANZE KU-CONFIGURE AU KU-ADD MATCH NA UPYA HAPANA KWA KUTUMIA HII INSTANCE HAPA UNAWEZA UKA-ENDA UKA-ITUMIA KU-ENDELEZA MATCH AMBAYO BADO HAIJAISHA... KO THAT
# WHAT WE NEED THIS SHOULD BE DISPLAYED IN USER MATCH SECTION IF ITS NOT COMPLETED AND THE PREVIEW/BROADCAST LINK FOR MATCH WHICH IS NOT COMPLETED SHOULD MADE AVAILABLE... 
# HIVYO MWANANGU.... BUT USIJE UKAJICHANGANYA IN SHORT USER HAWEZI AKA-BROADCAST MATCH MBILI KWA WAKATI MMOJA IN THE SAME APPLICATION.. KO HII INA-MAANA HATA KAMA ALIKUWA NA
# MATCH HAJAI-COMPLETE THEN INABIDI AI-COMPETE KWANZA NDO AANZISHE MATCH NYINGINE COZ HIZI MATCH ZINATEGEMEA THE SAME 'PREVIEW' RESOURCES MOJA KO HUWEZI NAHISI WE PROGRAMMER 
# UNAELEWA NA COZ WE-CREATE FOR STANDARD ONE THEN THIS SCENARIO IS GOOD..... KO PREVIEW INAKUWA BADO INA-PREVIEW/SHOW MATCH IF ITS NOT CLOSED/COMPLETED..

class Match(models.Model):
    # we need to create a function outside for it to being called everytime an object is created if you hardcode this in field
    # like models.IntegerField(default=time.time()) this will hardcode and use the same value for all obj
    # for more view https://docs.djangoproject.com/en/4.1/ref/models/fields/
    def generate_time():
        return int(time.time() * 1000)


    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    # Hapa inabidi ujue coz hizi match zinabaki on the database then if you say onetoone here maanake mtu atashindwa ku-start a new match because kuna match ambayo ilikuaga imeisha
    # ambayo ina the same team instance.. Ko for this case its good here to use oneToMany/Foreign key
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away')
    # venue should be registered in the database.. And it needs you to provide only two fields.. venue_name and venue_address
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    match_name = models.CharField(max_length=400)
    starting_time = models.DateTimeField(blank=True, null=True) # Haina haja ya kuwa na starting time coz by default we mwenyewe ukiona match imeanza unaenda kule kwenye start button then una-start...
    is_completed = models.BooleanField(default=False)
    matchId = models.CharField(max_length=20)
    extraTime = models.BooleanField(default=False) # Hii itatusaidia kujua kama hii match in extra-time or not... Lakini hii naona sio ya muhimu tunaweza tuka-ihandle on the frontend context/state only ... But kwa ajili ya kutunza kumbukumbu inabidi iwepo ..
    addedAt = models.PositiveBigIntegerField(default=generate_time) # this return the number of nanoseconds since epoch https://stackoverflow.com/questions/5998245/how-do-i-get-the-current-time-in-milliseconds-in-python https://www.google.com/search?client=firefox-b-d&q=python+time_ns+uses
    # hii maanake tutakuwa tuna-reference hii integer since epoch of milliseconds kujua mechi hii ni latest or not..

    @property
    def hteamname(self):
        return self.home_team.name

    @property
    def hteamlogo(self):
        return self.home_team.logo.url

    @property
    def ateamname(self):
        return self.away_team.name
    
    @property
    def ateamlogo(self):
        return self.away_team.logo.url

    @property
    def stadium(self):
        return self.venue.name
  
    def __str__(self):
        return self.matchId