from rest_framework.serializers import ModelSerializer
from .models import User, Event, TestModel, Game, Match

class TestSerializer(ModelSerializer):
    class Meta:
        model = TestModel
        fields = ("id", "title")

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'joined_events', 'is_staff']

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class MatchSerializer(ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'