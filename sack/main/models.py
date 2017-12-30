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
    zipcode = models.ForeignKey('zipcode', on_delete=models.CASCADE)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    url_onlinestreet = models.URLField()
    city = models.CharField(max_length=255)
    schaalundmueller_district_id = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Area(TimeStampedModel):
    description = models.CharField(max_length=1000)
    bag_type = models.CharField(max_length=20, choices=(('gelb', 'gelb'),))
    collector = models.CharField(max_length=1000)
    district_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{} [{}]".format(self.description, self.dates.count())


class PickUpDate(TimeStampedModel):
    date = models.DateField()
    area = models.ForeignKey(Area, related_name='dates', on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return "{} {}".format(self.area, self.date)
