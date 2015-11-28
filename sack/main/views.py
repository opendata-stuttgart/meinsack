from rest_framework import generics

from .models import Street
from .serializers import ZipCodeDetailSerializer, ZipCodeListSerializer


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
