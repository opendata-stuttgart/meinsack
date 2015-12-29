import datetime
from rest_framework import viewsets, mixins, response
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import decorators
from rest_framework.exceptions import NotFound

from .models import Street, ZipCode, Area
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


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, dict):
            return renderers.JSONRenderer().render(data, media_type, renderer_context)
        return data


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
        try:
            data = self.queryset.get(name=name, zipcode__zipcode=zipcode)
        except Street.DoesNotExist:
            raise NotFound()
        serializer = StreetDetailSerializer(data)
        return response.Response(serializer.data)

    @decorators.detail_route(methods=['get'], renderer_classes=(PlainTextRenderer,))
    def ical(self, request, name, zipcode):
        from icalendar import Calendar, Event
        data = self.queryset.get(name=name, zipcode__zipcode=zipcode)
        district_id = data.schaalundmueller_district_id
        try:
            area = Area.objects.get(district_id=district_id)
        except Area.DoesNotExist:
            raise NotFound()
        cal = Calendar()
        cal.add('prodid', '-//Meinsack.click Generator -  //NONSGML//DE')
        cal.add('version', '0.01')
        cal.add('x-wr-calname', 'meinsack Abholtermine')
        cal.add('x-original-url', 'https://meinsack.click/')
        cal.add('x-wr-caldesc', area.description)
        for dt in area.dates.all():   # filter(date__gte=datetime.date.today()):
            start = dt.date
            event = Event()
            event.add('summary', 'Meinsack Abholtermin')
            event.add('dtstart', start)
            event.add('dtend', start + datetime.timedelta(days=1))
            cal.add_component(event)
        return Response(cal.to_ical())
