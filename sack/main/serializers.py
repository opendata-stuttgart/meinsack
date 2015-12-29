import datetime
from rest_framework import serializers, relations
from rest_framework.reverse import reverse

from .models import Street, ZipCode, Area


class StreetDetailSerializer(serializers.HyperlinkedModelSerializer):
    dates = serializers.SerializerMethodField()

    def get_dates(self, obj):
        try:
            area = Area.objects.get(district_id=obj.schaalundmueller_district_id)
        except Area.DoesNotExist:
            return []
        return [dt.date for dt in area.dates.filter(date__gte=datetime.date.today())]

    class Meta:
        model = Street
        fields = [
            'name', 'dates'
        ]
        read_only_fields = fields


class StreetNestedSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        view_name = 'street-detail'
        url_kwargs = {
            'name': obj.name,
            'zipcode': obj.zipcode.zipcode
        }
        url = reverse(view_name, kwargs=url_kwargs, request=self.context.get('request'))
        if url is None:
            return None

        return relations.Hyperlink(url, obj.name)

    def get_name(self, obj):
        return obj.name


class ZipCodeDetailSerializer(serializers.HyperlinkedModelSerializer):
    street = serializers.SerializerMethodField()

    def get_street(self, obj):
        for street in obj.street_set.all():
            yield StreetNestedSerializer(street, context=self.context).data

    class Meta:
        model = ZipCode
        fields = [
            'zipcode', 'street'
        ]
        read_only_fields = fields


class ZipCodeListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='zipcode-detail', read_only=True, lookup_field="zipcode"
    )

    class Meta:
        model = ZipCode
        fields = [
            'zipcode', 'url'
        ]
        read_only_fields = fields
