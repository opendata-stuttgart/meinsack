from rest_framework import generics

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


class ZipCodeView(generics.ListAPIView):
    authentication_classes = list()
    permission_classes = list()

    def get_serializer_class(self):
        if 'zipcode' in self.kwargs:
            return ZipCodeDetailSerializer
        return ZipCodeListSerializer

    def get_queryset(self):
        if 'zipcode' in self.kwargs:
            return Street.objects.filter(zipcode=self.kwargs['zipcode'])
        return Street.objects.distinct('zipcode').order_by('zipcode')
