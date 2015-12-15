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


class ZipCode(TimeStampedModel):
    zipcode = models.CharField(max_length=255)

    class Meta:
        ordering = ['zipcode']

    def __str__(self):
        return self.zipcode


class Street(TimeStampedModel):
    name = models.CharField(max_length=255)
    zipcode = models.ForeignKey('zipcode')
    district = models.ForeignKey('District')
    url_onlinestreet = models.URLField()
    city = models.CharField(max_length=255)
    schaalundmueller_api_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
