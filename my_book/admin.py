from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(SingleBet)
admin.site.register(Straight)
admin.site.register(Action)
admin.site.register(Parlay3)
admin.site.register(Parlay4)
