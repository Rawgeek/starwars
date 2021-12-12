from django.db import models

# Create your models here.
class SWCharacter(models.Model):
    """
    Stores reference to csv file downloaded from an API
    """
    file = models.FileField()
    rows_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)