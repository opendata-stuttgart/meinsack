from django.contrib import admin
from .models import District, Street, ZipCode, Area, PickUpDate


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'zipcode', 'city', 'schaalundmueller_district_id']
    list_filter = ['district', 'zipcode', 'schaalundmueller_district_id']
    search_fields = ['name', 'zipcode__zipcode', 'city']


@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ['zipcode']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass


@admin.register(PickUpDate)
class PickUpDateAdmin(admin.ModelAdmin):
    pass
