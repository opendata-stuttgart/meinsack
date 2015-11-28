from django.contrib import admin
from .models import District, Street, ZipCode


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'zipcode', 'city']
    list_filter = ['district', 'zipcode']


@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ['zipcode']
