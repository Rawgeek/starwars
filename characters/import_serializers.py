from datetime import datetime
from rest_framework import serializers

class SimpleDateField(serializers.CharField):
    def to_representation(self, value):
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        return parsed.strftime('%Y-%m-%d')
        

class CharactersSerializer(serializers.Serializer):
    name = serializers.CharField()
    height = serializers.CharField()
    mass = serializers.CharField()
    hair_color = serializers.CharField()
    skin_color = serializers.CharField()
    eye_color = serializers.CharField()
    birth_year = serializers.CharField()
    gender = serializers.CharField()
    homeworld = serializers.CharField(source='homeworld.name')
    date = SimpleDateField(source='edited')

