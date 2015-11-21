from django.contrib import admin
from .models import District, Street


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'zipcode', 'city']
    list_filter = ['district', 'zipcode']
