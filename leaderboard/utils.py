from leaderboard.models import LeaderboardUser, Record, Car, Track

def bind_steamid_with_discord_user(steam_id_64, discord_user_id, discord_user_name, force=False):
    user = LeaderboardUser.objects.get_or_create(steam_id_64=steam_id_64)
    
    if user.discord_user_id and not force:
        return None
    
    user.discord_user_id = discord_user_id
    user.discord_user_name = discord_user_name
    user.save()
    return user


def create_record(steam_id_64, assetto_name, milliseconds, track_id, car_id):
    user, created = LeaderboardUser.objects.get_or_create(steam_id_64=steam_id_64)
    user.assetto_name = assetto_name
    user.save()
    
    track = Track.objects.get(track_id=track_id)
    if not track:
        return None
    
    car = Car.objects.get(car_id=car_id)
    if not car:
        return None
    
    record = Record(user=user, milliseconds=milliseconds, track=track, car=car)
    record.save()
    return record


def get_top_records(track_id, car_id=None, limit=10):
    if car_id:
        return Record.objects.filter(track__track_id=track_id, car__car_id=car_id).order_by('milliseconds')[:limit]
    else:
        return Record.objects.filter(track__track_id=track_id).order_by('milliseconds')[:limit]


def get_user_top_records(discord_user_id, track_id, car_id=None, limit=10):
    if car_id:
        return Record.objects.filter(user__discord_user_id=discord_user_id, track__track_id=track_id, car__car_id=car_id).order_by('milliseconds')[:limit]
    else:
        return Record.objects.filter(user__discord_user_id=discord_user_id, track__track_id=track_id).order_by('milliseconds')[:limit]
