from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
import json
# from django.contrib.postgres.fields import ArrayField

# Create your models here.
class TestModel(models.Model):
    title = models.CharField(max_length=20)



class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class Game(models.Model):
    name = models.CharField(max_length=15)
    fields = models.JSONField()


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length = 15)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    joined_events = models.ManyToManyField('Event', default=None, blank=True)
    game_stats = models.JSONField(blank=True, null=True, default=dict)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_module_perms(self, perm, obj=None):
        return self.is_superuser
    
    def has_perm(self, perm):
        return self.is_superuser
    

Games = [
    ('eFootball', 'eFootball'),
    ('BGMI', 'BGMI'),
    ('CODM', 'CODM'),
    ('FREE FIRE', 'FREE FIRE')
]

EVENT_TYPES = [
    ('knockout', 'knockout'),
    ('league', 'league')
]

EVENT_STATE = [
    ("active", "active"),
    ("started", "started"),
    ("ended", "ended"),
    ("pending", "pending")
]

MATCH_STATE = [
    ("pending", "pending"),
    ("ended", "ended"),
    ("active", "active")
]

REWARD_TYPE = [
    ("money", "money"),
    ("credit", "credit"),
    ("other", "other")
]




class Match(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='matches_as_player1', blank=True, null=True)
    player2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='matches_as_player2', blank=True, null=True)
    matchgame = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name="matches")
    matchstate = models.CharField(max_length=10, choices=MATCH_STATE, default="pending")
    matchwinner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="matches_won", null=True, blank=True)
    round = models.IntegerField(null=True, blank=True)
    root = models.IntegerField(null=True, blank=True)
    player1stats = models.JSONField(blank=True, null=True, default=dict)
    player2stats = models.JSONField(blank=True, null=True, default=dict)

class Event(models.Model):
    title = models.CharField(max_length=30)
    img = models.ImageField(upload_to="./media/", null=True, blank=True)
    details = models.TextField(max_length=500)
    rules = models.TextField(max_length=500)
    eventgame = models.ForeignKey(Game, related_name="events", on_delete=models.DO_NOTHING)
    eventhost = models.CharField(max_length=20)
    eventplayers = models.ManyToManyField('User', blank=True)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES, default="knockout")
    event_state = models.CharField(max_length=10, choices=EVENT_STATE, default="active")
    winner_reward = models.CharField(max_length=10)
    runner_reward = models.CharField(max_length=10)
    third_reward = models.CharField(max_length=10)
    reward_type = models.CharField(max_length=10, choices=REWARD_TYPE)
    max_players = models.IntegerField()
    matches = models.ManyToManyField(Match, blank=True)
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="events_won")
    runner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="events_runner")
    third = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="events_third")