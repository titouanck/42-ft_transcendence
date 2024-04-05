from django.contrib import admin

# Register your models here.
from .models.Player import Player
from .models.Pongtoken import Pongtoken
from .models.Match import Match

# Register your models here.
admin.site.register(Player)
admin.site.register(Pongtoken)
admin.site.register(Match)