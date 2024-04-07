from django.contrib import admin

# Register your models here.
from .models.Player import Player
from .models.Match import Match
from .models.Tournament import Tournament
from .models.TournamentRound import TournamentRound
from .models.TournamentRound import TournamentRound
from .models.EmailVerification import EmailVerification

# Register your models here.
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Tournament)
admin.site.register(TournamentRound)
admin.site.register(EmailVerification)
