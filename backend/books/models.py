from django.db import models

import uuid

# Create your models here.

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    isbn_number = models.CharField(max_length=13, unique=True)
    cover_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
