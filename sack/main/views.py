import datetime
from rest_framework import viewsets, mixins, response
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import decorators
from rest_framework.exceptions import NotFound
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.core.urlresolvers import reverse

from .models import Street, ZipCode, Area
from .serializers import ZipCodeDetailSerializer, ZipCodeListSerializer, StreetDetailSerializer

from django import forms


class GetIcalForm(forms.Form):
    zipcode = forms.CharField(max_length=10)
    street = forms.CharField(max_length=100)


class GetIcalView(FormView):
    template_name = 'home.html'
    form_class = GetIcalForm
    success_url = '/'

    def post(self, request):
        context = self.get_context_data()
        form = self.get_form(self.form_class)
        if form.is_valid():
            zipcode = form.cleaned_data['zipcode']
            street = form.cleaned_data['street']
            context['ical_url'] = reverse('street-ical', kwargs={'zipcode': zipcode,
                                                                 'name': street})
        return render(self.request, self.template_name, context)


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
        qs = ZipCode.objects.distinct('zipcode').order_by('zipcode')
        if not 'zipcode' in self.kwargs:
            zipcode_filter = self.request.query_params.get('zipcode', None)
            if zipcode_filter is not None:
                return qs.filter(zipcode__icontains=zipcode_filter)
        return qs


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
        try:
            data = self.queryset.get(name=name, zipcode__zipcode=zipcode)
        except Street.DoesNotExist:
            raise NotFound()
        except Street.MultipleObjectsReturned:
            data = self.queryset.filter(name=name, zipcode__zipcode=zipcode).first()
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
        for dt in area.dates.filter(date__gte=datetime.date.today()):
            start = dt.date
            event = Event()
            event.add('summary', 'Meinsack Abholtermin')
            event.add('dtstart', start)
            event.add('dtend', start + datetime.timedelta(days=1))
            cal.add_component(event)
        return Response(cal.to_ical())
