from django.db import models
from django_extensions.db.models import TimeStampedModel                                  
# Create your models here.
class District(TimeStampedModel):
    name = models.CharField(
            max_length=255)
    city = models.CharField(
            max_length=255)
    number_of_streets = models.IntegerField()
    url_onlinestreet = models.URLField()
