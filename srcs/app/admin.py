from django.contrib import admin

# Register your models here.
from .models import Player, Pongtoken, Match

# Register your models here.
admin.site.register(Player)
admin.site.register(Pongtoken)
admin.site.register(Match)