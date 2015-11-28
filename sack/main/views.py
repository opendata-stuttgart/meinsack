from rest_framework import viewsets, mixins

from .models import Street
from .serializers import ZipCodeDetailSerializer, ZipCodeListSerializer


class ZipCodeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'zipcode'
    authentication_classes = list()
    permission_classes = list()

    def get_serializer_class(self):
        if 'zipcode' in self.kwargs:
            return ZipCodeDetailSerializer
        return ZipCodeListSerializer

    def get_object(self):
        if 'zipcode' in self.kwargs:
            return Street.objects.filter(zipcode=self.kwargs['zipcode']).first()
        return None

    def get_queryset(self):
        return Street.objects.distinct('zipcode').order_by('zipcode')
