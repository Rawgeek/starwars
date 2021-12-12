import os
import petl as etl
import uuid

from django.core.files.storage import default_storage
from django.core.files import File

from .client import SWAPIClient
from .import_serializers import CharactersSerializer
from .models import SWCharacter

def download_characters():
    client = SWAPIClient()
    people = client.get_people()
    data = CharactersSerializer(people, many=True).data

    full_path = ".{}{}.csv".format(default_storage.base_url, str(uuid.uuid1()))
    table = etl.fromdicts(data)
    table.tocsv(full_path)

    with open(full_path, 'rb') as fi:
        file = File(fi, name=os.path.basename(fi.name))
        SWCharacter.objects.create(file=file, rows_count=len(data))

def parse_csv_with_characters(file_path):
    table = etl.fromcsv(file_path)
    return table
