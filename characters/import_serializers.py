from rest_framework import serializers

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
    date = serializers.DateTimeField(source='created')

