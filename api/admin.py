from django.contrib import admin
from .models import User, Event, Game, Match
# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Game)
admin.site.register(Match)