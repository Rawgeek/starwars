from django.utils.functional import cached_property
from django.db import models

# Create your models here.
class CharactersDocument(models.Model):
    """
    Stores reference to csv file downloaded from an API
    """
    file = models.FileField()
    rows_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    @cached_property
    def table(self):
        from .services import parse_csv_with_characters
        return parse_csv_with_characters(self.file)

    @cached_property
    def header(self):
        from .services import get_header
        return get_header(self.table)

    @cached_property
    def data(self):
        return self.table.data()
