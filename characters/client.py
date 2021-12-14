import logging
import requests

from urllib.parse import urlparse, parse_qs
from rest_framework import status
from django.conf import settings

logger = logging.getLogger(__name__)

class SWAPIClient:
    _cache = {}

    def __init__(self, populate_related=True, download_all=True, enable_cache=True):
        self._base_url = settings.SWAPI_URL
        self._populate_related = populate_related
        self._download_all = download_all
        self._enable_cache = enable_cache

    def _parse_response(self, response):
        data = response.json()
        return data

    def _get_resorce_name_and_id(self, path):
        path, params = self._parse_relative_url(path)
        resource = path.split('/')[0]
        id = path.split('/')[1]
        return resource, id

    def _store_cache(self, url, data):
        resource, id = self._get_resorce_name_and_id(url)
        if resource not in self._cache:
            self._cache.update({resource: {}})
        self._cache[resource].update({
            id: data
        })

    def _parse_relative_url(self, url):
        url = url.replace(self._base_url, '')
        next_params = parse_qs(urlparse(url).query)
        next_path = urlparse(url).path
        return next_path, next_params

    def _is_local_url(self, url):
        return isinstance(url, str) and self._base_url in url

    def get_from_cache(self, resource, id):
        if resource in self._cache and id in self._cache[resource]:
            return self._cache[resource][id]

    def populate_resource(self, r):
        for (k, v) in r.items():
            if not k == 'url' and self._is_local_url(v):
                resource, id = self._get_resorce_name_and_id(v)
                r[k] = self.get_details(resource, id)
        return r

    def get(self, url, params=None, parse=True):
        response = requests.request('get', url, params=params)
        # logger.info(url, params, response)
        print(url, params, response)
        if response.status_code is not status.HTTP_200_OK:
            raise Exception("Error while fetching %s, status code %s", url, response.status_code)
        if parse:
            return self._parse_response(response)
        else:
            return response

    def get_details(self, resource_path, id):
        data = self.get_from_cache(resource_path, id)
        if data:
            return data
        url = "{}{}/{}".format(self._base_url, resource_path, id)
        data = self.get(url)
        if self._enable_cache:
            self._store_cache(data.get('url'), data)
        return data
        
    def get_all(self, resource_path, params=None):
        url = "{}{}/".format(self._base_url, resource_path)
        data = self.get(url, params)

        if 'results' in data and self._download_all and data.get('next'):
            next_path, next_params = self._parse_relative_url(data.get('next'))
            data['results'] += self.get_all(resource_path, next_params)
        if self._enable_cache:
            for r in data['results']:
                r = self.populate_resource(r)
                self._store_cache(r.get('url'), r)
        return data['results']

    def get_people(self):
        """
        GET https://swapi.dev/api/people/
        """
        self.get_planets() # Optimized prefetch
        return self.get_all('people')

    def get_planets(self):
        """
        GET https://swapi.dev/api/planets/
        """
        return self.get_all('planets')

    def get_species(self):
        """
        GET https://swapi.dev/api/species/
        """
        return self.get_all('species')

    def get_films(self):
        """
        GET https://swapi.dev/api/films/
        """
        return self.get_all('films')