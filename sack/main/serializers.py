from rest_framework import serializers

from .models import Street


class ZipCodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = [
            'zipcode', 'city'
        ]
        read_only_fields = fields


class ZipCodeDetailSerializer(serializers.ModelSerializer):
    street = serializers.SerializerMethodField()

    def get_street(self, obj):
        return obj.name

    class Meta:
        model = Street
        fields = [
            'zipcode', 'city', 'street'
        ]
        read_only_fields = fields
