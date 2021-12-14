from rest_framework import viewsets

from .serializers import SWCharacterGroupedSerializer, SWCharacterSerializer, SWCharacterDetailsSerializer
from .models import CharactersDocument
from .services import download_characters

class CharacterDocumentsViewSet(viewsets.ModelViewSet):
    serializer_class = SWCharacterSerializer
    queryset = CharactersDocument.objects.all()

    def perform_create(self, serializer):
        download_characters()

class CharacterDocumentDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = SWCharacterDetailsSerializer
    queryset = CharactersDocument.objects.all()
    
    def get_serializer_class(self):
        if self.request.query_params.get('group_by'):
            return SWCharacterGroupedSerializer
        else:
            return SWCharacterDetailsSerializer 