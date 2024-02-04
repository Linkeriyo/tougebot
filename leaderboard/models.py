from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class LeaderboardUser(models.Model):
    steam_id_64 = models.CharField(max_length=20, unique=True)
    assetto_name = models.CharField(max_length=32)
    discord_user_id = models.CharField(max_length=20, unique=True)
    discord_user_name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.discord_user_name)


class Record(models.Model):
    user = models.ForeignKey('LeaderboardUser', on_delete=models.CASCADE)
    milliseconds = models.IntegerField(validators=[MinValueValidator(0)])
    datetime = models.DateTimeField(auto_now_add=True)
    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)

    def __str__(self):
        displaytime = milliseconds_to_displaytime(self.milliseconds)
        return f"{self.user.discord_user_name} - {displaytime} - {self.track.track_name} - {self.car.car_name}"


class Track(models.Model):
    track_id = models.CharField(max_length=100)
    track_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.track_name)


class Car(models.Model):
    car_id = models.CharField(max_length=100)
    car_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.car_name)


def milliseconds_to_displaytime(milliseconds):
    hours = milliseconds // 3600000
    milliseconds %= 3600000
    minutes = milliseconds // 60000
    milliseconds %= 60000
    seconds = milliseconds // 1000
    milliseconds %= 1000
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def displaytime_to_milliseconds(displaytime):
    hours, minutes, seconds = displaytime.split(":")
    seconds, milliseconds = seconds.split(".")
    return int(hours) * 3600000 + int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds)
