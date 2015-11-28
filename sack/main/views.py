from rest_framework import viewsets, mixins, response

from .models import Street, ZipCode
from .serializers import ZipCodeDetailSerializer, ZipCodeListSerializer, StreetDetailSerializer


class ZipCodeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'zipcode'
    authentication_classes = list()
    permission_classes = list()

    def get_serializer_class(self):
        if 'zipcode' in self.kwargs:
            return ZipCodeDetailSerializer
        return ZipCodeListSerializer

    def get_queryset(self):
        return ZipCode.objects.distinct('zipcode').order_by('zipcode')


class StreetViewSet(mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    lookup_field = 'name'
    authentication_classes = list()
    permission_classes = list()
    queryset = Street.objects.all()

    def get_serializer_class(self):
        return ZipCodeDetailSerializer

    def get_object(self):
        if 'zipcode' in self.kwargs:
            return Street.objects.filter(zipcode=self.kwargs['zipcode']).first()
        return None

    def retrieve(self, request, name=None, zipcode=None):
        data = self.queryset.get(name=name, zipcode__zipcode=zipcode)
        serializer = StreetDetailSerializer(data)
        return response.Response(serializer.data)
