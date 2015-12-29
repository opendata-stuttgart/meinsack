# coding=utf-8
from django.core.management import BaseCommand
from main.models import Street, Area, PickUpDate
from main.utils import call_schaal_und_mueller_district
import datetime


class Command(BaseCommand):

    help = "schaal+mueller districts"

    def handle(self, *args, **options):
        l = Street.objects.order_by('schaalundmueller_district_id').distinct('schaalundmueller_district_id').values_list('schaalundmueller_district_id', flat=True)
        for num in l:
            if num:
                d = call_schaal_und_mueller_district(num)
                area, created = Area.objects.get_or_create(description=d['area'],
                                                           bag_type="gelb",
                                                           collector="Schaal+Mueller",
                                                           district_id=num)
                for _ in d['dates']:
                    dt = datetime.datetime.strptime(_, "%d.%m.%Y").date()
                    pickupdate, created = PickUpDate.objects.get_or_create(date=dt,
                                                                           area=area)
                    print(pickupdate)
