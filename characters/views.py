from rest_framework import viewsets

from .serializers import SWCharacterSerializer, SWCharacterDetailsSerializer
from .models import SWCharacter
from .services import download_characters

class CharacterDocumentsViewSet(viewsets.ModelViewSet):
    serializer_class = SWCharacterSerializer
    queryset = SWCharacter.objects.all()

    def perform_create(self, serializer):
        download_characters()

class CharacterDocumentDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = SWCharacterDetailsSerializer
    queryset = SWCharacter.objects.all()
    