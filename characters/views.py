from rest_framework import viewsets

from .serializers import SWCharacterSerializer, SWCharacterDetailsSerializer
from .models import SWCharacter

class CharacterDocumentsViewSet(viewsets.ModelViewSet):
    serializer_class = SWCharacterSerializer
    queryset = SWCharacter.objects.all()

class CharacterDocumentDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = SWCharacterDetailsSerializer
    queryset = SWCharacter.objects.all()
    