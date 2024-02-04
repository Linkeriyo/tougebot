from django.contrib import admin
from leaderboard import models

# Register your models here.
admin.site.register(models.LeaderboardUser)
admin.site.register(models.Record)
admin.site.register(models.Track)
admin.site.register(models.Car)
