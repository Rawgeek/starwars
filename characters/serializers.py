from rest_framework import serializers

from .models import SWCharacter
from .services import parse_csv_with_characters

class SWCharacterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='file.name')

    class Meta:
        fields = (
            'id',
            'name',
            'file',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'name',
            'file',
            'created_at',
            'updated_at',
        )
        model = SWCharacter

class SWCharacterDetailsSerializer(SWCharacterSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'rows_count',
            'data',
            'file',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'name',
            'rows_count',
            'data',
            'file',
            'created_at',
            'updated_at',
        )
        model = SWCharacter

    def get_data(self, obj):
        request = self.context['request']
        offset = int(request.query_params.get('offset') or 0)
        limit = offset + 10
        return parse_csv_with_characters(obj.file).tol()[offset:limit]