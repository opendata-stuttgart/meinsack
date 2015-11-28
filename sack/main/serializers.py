from rest_framework import serializers

from .models import Street


class ZipCodeListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='zipcode-detail', read_only=True, lookup_field="zipcode"
    )

    class Meta:
        model = Street
        fields = [
            'zipcode', 'city', 'url'
        ]
        read_only_fields = fields


class ZipCodeDetailSerializer(serializers.HyperlinkedModelSerializer):
    street = serializers.SerializerMethodField()

    def get_street(self, obj):
        return [i.name for i in Street.objects.filter(zipcode=obj.zipcode).order_by('name')]

    class Meta:
        model = Street
        fields = [
            'zipcode', 'city', 'street'
        ]
        read_only_fields = fields
