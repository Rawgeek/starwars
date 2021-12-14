from rest_framework import serializers

from .models import CharactersDocument
from .services import get_grouped_count_table

class SWCharacterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='file.name', required=False)

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
        model = CharactersDocument

class SWCharacterDetailsSerializer(SWCharacterSerializer):
    data = serializers.SerializerMethodField()
    header = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        fields = (
            'id',
            'name',
            'rows_count',
            'data',
            'header',
            'file',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'name',
            'rows_count',
            'data',
            'header',
            'file',
            'created_at',
            'updated_at',
        )
        model = CharactersDocument

    def get_data(self, obj):
        request = self.context['request']
        offset = int(request.query_params.get('offset') or 0)
        limit = offset + 10
        return obj.data[offset:limit]

class SWCharacterGroupedSerializer(SWCharacterSerializer):
    data = serializers.SerializerMethodField()
    header = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'data',
            'header',
        )
        read_only_fields = (
            'id',
            'name',
            'data',
            'header',
        )
        model = CharactersDocument

    def get_group_by(self, obj):
        request = self.context['request']
        group_by = request.query_params.get('group_by').split(',') or obj.header
        if not isinstance(group_by, list):
            return [group_by]
        return group_by

    def get_data(self, obj):
        group_by = self.get_group_by(obj)
        return get_grouped_count_table(obj.table, group_by).data().tol()

    def get_header(self, obj):
        group_by = self.get_group_by(obj)
        return get_grouped_count_table(obj.table, group_by).header()