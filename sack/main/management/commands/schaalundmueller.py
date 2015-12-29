# coding=utf-8
from django.core.management import BaseCommand
from main.models import Street
from main.utils import call_schaal_und_mueller_for_district_id


class Command(BaseCommand):

    help = "schaal+mueller id crawling"

    def handle(self, *args, **options):
        for street in Street.objects\
                            .filter(city__contains="Stuttgart")\
                            .filter(schaalundmueller_district_id__isnull=True):
            print(street.pk),
            print(street.name)
            call_schaal_und_mueller_for_district_id(street)
