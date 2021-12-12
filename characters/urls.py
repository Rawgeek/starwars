from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import CharacterDocumentsViewSet, CharacterDocumentDetailsViewSet

app_name = 'character_document_api'

list_actions = {'get': 'list', 'post': 'create'}
detail_actions = {'get': 'retrieve',}

urlpatterns = [
    url(r'^$', CharacterDocumentsViewSet.as_view(list_actions), name='list'),
    url(r'^(?P<pk>\d+)$', CharacterDocumentDetailsViewSet.as_view(detail_actions), name='details'),
]

router = SimpleRouter()

urlpatterns += router.get_urls()
