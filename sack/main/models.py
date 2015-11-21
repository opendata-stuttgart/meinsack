from django.db import models
from django_extensions.db.models import TimeStampedModel


class District(TimeStampedModel):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    number_of_streets = models.IntegerField()
    url_onlinestreet = models.URLField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Street(TimeStampedModel):
    name = models.CharField(max_length=255)
    district = models.ForeignKey('District')
    url_onlinestreet = models.URLField()
    zipcode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
