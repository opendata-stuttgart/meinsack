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


class ZipCodeListView(generics.ListAPIView):
    authentication_classes = list()
    permission_classes = list()
    serializer_class = ZipCodeListSerializer

    def get_queryset(self):
        return Street.objects.distinct('zipcode').order_by('zipcode')


class ZipCodeDetailView(generics.ListAPIView):
    authentication_classes = list()
    permission_classes = list()
    serializer_class = ZipCodeDetailSerializer

    def get_queryset(self):
        return Street.objects.filter(zipcode=self.kwargs['zipcode'])
