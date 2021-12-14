import os
import json

from unittest.mock import patch
from freezegun import freeze_time
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.conf import settings
from django.urls import reverse

from ..client import SWAPIClient
from ..import_serializers import CharactersSerializer
from ..services import download_characters, get_grouped_count_table
from ..models import CharactersDocument


def mocked_requests_get(*args, **kwargs):
    def load_fixture(name, format='json'):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = '{}.{}'.format(name, format)

        fixture_path = os.path.join(dir_path, 'fixtures', file_name)
        with open(fixture_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    
    if args[0] == 'get':
        if args[1] == f'{settings.SWAPI_URL}people/':
            params = kwargs.get('params', {})
            if params:
                page = params.get('page', [])
                if page and page[0] == '2':
                    return MockResponse(load_fixture('people2'), 200)
            return MockResponse(load_fixture('people'), 200)
        if args[1] == f'{settings.SWAPI_URL}planets/':
            return MockResponse(load_fixture('planets'), 200)
        if args[1] == f'{settings.SWAPI_URL}planets/20':
            return MockResponse(load_fixture('planet'), 200)

    return MockResponse(None, 404)

class SWClientTest(TestCase):
    @patch('characters.client.requests.request', side_effect=mocked_requests_get)
    def test_fetching_people(self, mock_get):
        client = SWAPIClient()
        characters = client.get_people()

        person1 = list(filter(lambda person: person['name'] == 'Wilhuff Tarkin', characters))[0]
        self.assertEquals(person1.get('homeworld', {}).get('name'), "Alderaan")
        self.assertEquals(person1.get('birth_year'), "64BBY")

        person2 = list(filter(lambda person: person['name'] == 'Obi-Wan Kenobi', characters))[0]
        self.assertEquals(person2.get('homeworld', {}).get('name'), "Stewjon")
        self.assertEquals(person2.get('birth_year'), "57BBY")


class CharactersImportSerializerTest(TestCase):
    @patch('characters.client.requests.request', side_effect=mocked_requests_get)
    def test_serializing_people(self, mock_get):
        client2 = SWAPIClient()
        characters = client2.get_people()

        serialized_data = CharactersSerializer(characters, many=True).data
        
        person1 = list(filter(lambda person: person['name'] == 'Wilhuff Tarkin', serialized_data))[0]

        self.assertEquals(person1.get('homeworld', {}), "Alderaan")
        self.assertEquals(person1.get('birth_year'), "64BBY")
        self.assertEquals(person1.get('date'), "2014-12-20")

        person2 = list(filter(lambda person: person['name'] == 'Obi-Wan Kenobi', serialized_data))[0]
        self.assertEquals(person2.get('homeworld', {}), "Stewjon")
        self.assertEquals(person2.get('birth_year'), "57BBY")
        self.assertEquals(person2.get('date'), "2014-12-20")


class CharactersServicesTest(TestCase):
    @patch('characters.client.requests.request', side_effect=mocked_requests_get)
    def setUp(self, mock_get):
        download_characters()
        self.document = CharactersDocument.objects.last()

    def test_document_creation(self):
        self.assertEquals(CharactersDocument.objects.count(), 1)
        self.assertEquals(self.document.rows_count, 20)
        self.assertEquals(len(self.document.data), 20)
        self.assertIsNotNone(self.document.file)
        self.assertIsNotNone(self.document.created_at)
        self.assertIsNotNone(self.document.updated_at)
        self.assertEquals(self.document.header, 
            ('name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year', 'gender', 'homeworld', 'date'))
    
    def test_grouping_sinlge(self):
        grouped_table = get_grouped_count_table(self.document.table, 'gender')
        self.assertEquals(grouped_table.data().tol(), 
            (['male', 14],
            ['n/a', 3],
            ['female', 2],
            ['hermaphrodite', 1]))
        
    def test_grouping_multiple(self):
        grouped_table = get_grouped_count_table(self.document.table, ['gender', 'homeworld'])
        self.assertEquals(grouped_table.data().tol(), 
            (['male', 'Tatooine', 8],
            ['male', 'Alderaan', 2],
            ['n/a', 'Tatooine', 2],
            ['female', 'Alderaan', 1],
            ['female', 'Tatooine', 1],
            ['hermaphrodite', 'Tatooine', 1],
            ['male', 'Hoth', 1],
            ['male', 'Naboo', 1],
            ['male', 'Stewjon', 1],
            ['male', 'Yavin IV', 1],
            ['n/a', 'Naboo', 1]))
        

@freeze_time("2021-11-11")
class APITest(APITestCase):
    @patch('characters.client.requests.request', side_effect=mocked_requests_get)
    def setUp(self, mock_get):
        download_characters()
        self.document = CharactersDocument.objects.last()
        self.url = reverse('character_document_api:list')
        self.data = [{
            "id": 1, 
            "name": self.document.file.name, 
            "file": f'http://testserver/media/{self.document.file.name}', 
            "created_at": "2021-11-11T00:00:00Z", 
            "updated_at": "2021-11-11T00:00:00Z"}]

    def test_url(self):
        self.assertEqual(self.url, '/api/documents/')

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.dumps(response.data), json.dumps(self.data))

    @patch('characters.client.requests.request', side_effect=mocked_requests_get)
    def test_create(self, mock_get):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CharactersDocument.objects.count(), 2)

    def test_get(self):
        url = reverse('character_document_api:details', kwargs={"pk": self.document.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
