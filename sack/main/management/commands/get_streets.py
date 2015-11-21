# coding=utf-8
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Import streets and districts"

    def handle(self, *args, **options):
        from main.utils import get_districts_stuttgart, extract_district_from_tr, add_district_to_database, get_streets_from_district, extract_street_from_tr, add_street_to_database 

        foo = False
        for tr in get_districts_stuttgart():
            d = extract_district_from_tr(tr)
            district = add_district_to_database(d)
            for street in get_streets_from_district(district):
                data = extract_street_from_tr(street)
                street = add_street_to_database(data, district)
